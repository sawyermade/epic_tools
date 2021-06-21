import sys, os, numpy as np, time, gulpio, compress_json, re, json, time
from tqdm import tqdm

def get_missing(seg_list, seg_output_list):
	missing_segs, missing_index = [], []
	for i, seg in enumerate(seg_list):
		if not seg in seg_output_list:
			missing_segs.append(seg)
			missing_index.append(i)

	return missing_segs, missing_index

def read_gulp(gulp_dir):
	# Read gulp directory
	gd = gulpio.GulpDirectory(gulp_dir)

	# Get list of segments from meta data and 3 value/level stable sort
	reg = r'^P([0-9]+)_([0-9]+)_([0-9]+)$'
	match_list = sorted(
		[re.match(reg, s) for s in gd.chunk_lookup.keys()], 
		key=lambda x: (int(x.group(1)), int(x.group(2)), int(x.group(3)))
	)
	seg_list = [s.group(0) for s in match_list]
	
	# Return segment id list and gulp directory
	return (gd, seg_list)

def read_dets(dets_dir, seg_list):
	# Gets json file list from directory
	dets_list = os.listdir(dets_dir)

	# Sorts dets files list
	reg = r'^P([0-9]+)_([0-9]+)_([0-9]+).json.bz$'
	match_list = sorted(
		[re.match(reg, s) for s in dets_list], 
		key=lambda x: (int(x.group(1)), int(x.group(2)), int(x.group(3)))
	)
	dets_list = [s.group(0) for s in match_list]

	# Create path list
	dets_path_list = [os.path.join(dets_dir, f) for f in dets_list]

	# Checks for missing
	dets_list_no_ext = [f.replace('.json.bz', '') for f in dets_list]
	missing_segs, missing_index = get_missing(seg_list, dets_list_no_ext)
	if missing_segs:
		print(f'missing segment detections and indices:\nMissing Segs:\n{missing_segs}\nMissing Indices:\n{missing_index}\n')
		sys.exit(0)
	else:
		return dets_path_list

def thresh_dets(dets_path, thresh=0.50):
	# Opens detections and gets frames
	frame_dict = compress_json.load(dets_path)
	frames = sorted([int(f) for f in frame_dict.keys()])
	thresh_frame_dict = {}
	class_freq = [0] * 291
	
	# Goes through each frames detections
	for frame in frames:
		# Gets detection information
		#dets keys: 'detection_scores', 'detection_boxes', 'num_detections', 'detection_classes'
		dets = frame_dict[str(frame)]
		dets_scores = np.asarray(dets['detection_scores'])
		dets_classes = dets['detection_classes']
		dets_boxes = dets['detection_boxes']
		# print(len(dets_classes))

		# Thresholds only dets >= to threshold
		dets_indices = np.where(dets_scores >= thresh)[0]
		dets_scores = [v for i, v in enumerate(dets_scores) if i in dets_indices]
		dets_classes = [v for i, v in enumerate(dets_classes) if i in dets_indices]
		dets_boxes = [v for i, v in enumerate(dets_boxes) if i in dets_indices]

		# Gets dets center points
		dets_centers = []
		for box in dets_boxes:
			ymin, xmin, ymax, xmax = box
			cy = ymin + ((ymax - ymin) / 2.0)
			cx = xmin + ((xmax - xmin) / 2.0)
			dets_centers.append([cy, cx])

		# Adds to thresh dict
		thresh_frame_dict[str(frame)] = {
			'detection_scores' : dets_scores,
			'detection_classes' : dets_classes,
			'detection_centers' : dets_centers
		}

		# Class frequency
		for c in dets_classes:
			class_freq[c] += 1

	return thresh_frame_dict, np.asarray(class_freq)

def main():
	# Args
	gulp_dir = sys.argv[1]
	dets_dir = sys.argv[2]
	out_dir = sys.argv[3]
	if len(sys.argv) > 4: 
		thresh = float(sys.argv[4])
	else: 
		thresh = 0.50
	label_dict = json.load(open('label_map.json'))

	# Create output dir
	out_dir = f'{out_dir}-{thresh}'
	if not os.path.exists(out_dir): 
		os.makedirs(out_dir)

	# Get gulped stuff
	gd, seg_list = read_gulp(gulp_dir)

	# Get dets file list
	dets_path_list = read_dets(dets_dir, seg_list)
	print(f'seg_list, dets_path_list length: {len(seg_list)}, {len(dets_path_list)}\n')

	# Timer Start
	time_start = time.perf_counter()

	# Threshold dets
	top_1, top_3, top_5 = 0, 0, 0
	for i, dets_path in enumerate(dets_path_list):
		# Gets thresholded dets and class freq
		thresh_frame_dict, class_freq = thresh_dets(dets_path, thresh)
		fname = os.path.split(dets_path)[-1]
		seg_id = fname.replace('.json.bz', '')

		# Compares to ground truth nouns
		_, meta = gd[seg_id]
		noun_gt = meta['noun']
		noun_dets_classes = np.where(class_freq > 0)[0]
		noun_dets = [(label_dict[str(i)], class_freq[i]) for i in noun_dets_classes]
		noun_dets.sort(key=lambda x: x[1], reverse=True)
		print(f'Segment: {i}')
		print(f'noun_gt: {noun_gt}')
		print(f'noun_dets (label, freq): {noun_dets}\n')

		# Saves thresholded detections
		out_path = os.path.join(out_dir, fname)
		compress_json.dump(thresh_frame_dict, out_path)

		# Top 1, 3, 5 comparison
		# if len(noun_dets) > 0: 
		# 	noun_dets_1 = noun_dets[0][0]
		# else:
		# 	noun_dets_1 = None

		# if len(noun_dets) >= 3: 
		# 	noun_dets_3 = noun_dets[:3][0]
		# else:
		# 	noun_dets_3 = None

		# if len(noun_dets) >= 5: 
		# 	noun_dets_5 = noun_dets[:5][0]
		# else:
		# 	noun_dets_5 = None

	# Timer End
	time_stop = time.perf_counter()
	print(f'Inference time to run: {round(time_stop - time_start, 2)}s')


if __name__ == '__main__':
	main()