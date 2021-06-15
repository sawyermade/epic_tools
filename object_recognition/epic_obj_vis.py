import sys, os, numpy as np, gulpio, compress_json, re, cv2, json

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

def main():
	# Args
	gulp_dir = sys.argv[1]
	dets_dir = sys.argv[2]

	# Get gulped stuff
	gd, seg_list = read_gulp(gulp_dir)

	# Get dets files
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

	# Gets single frame and bboxes
	#dets keys: 'detection_scores', 'detection_boxes', 'num_detections', 'detection_classes'
	box_num = 2
	frame_dict = compress_json.load(dets_path_list[0])
	frame_list = sorted([int(f) for f in frame_dict.keys()])
	bbox = frame_dict[str(frame_list[0])]['detection_boxes'][box_num]
	bbox_class = frame_dict[str(frame_list[0])]['detection_classes'][box_num]
	frames, meta = gd[dets_list[0].replace('.json.bz', '')]
	frame = frames[0]
	dim_y, dim_x, _ = frame.shape
	label_dict = json.load(open('label_map.json'))
	
	# cx, cy, w, h = bbox
	# cx, cy, w, h = int(cx*dim_x), int(cy*dim_y), int(w*dim_x), int(h*dim_y)
	# x = cx - (w//2)
	# y = cy - (h//2)
	# x0, y0, x1, y1 = bbox
	y0, x0, y1, x1 = bbox
	x0, y0, x1, y1 = int(x0*dim_x), int(y0*dim_y), int(x1*dim_x), int(y1*dim_y)
	cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
	cv2.imshow("bbox", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	print(f'bbox_class: {bbox_class}')
	print(f'bbox: {bbox}')
	print(f'dim x, y: {dim_x}, {dim_y}')
	print(f'label: {label_dict[str(bbox_class)]}')
	print(f'frame_list')


if __name__ == '__main__':
	main()