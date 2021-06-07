import sys, os, numpy as np, time, gulpio, compress_json, re
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

def main():
	# Args
	gulp_dir = sys.argv[1]
	dets_dir = sys.argv[2]

	# Get gulped stuff
	gd, seg_list = read_gulp(gulp_dir)

	# Get dets file list
	dets_path_list = read_dets(dets_dir, seg_list)
	print(f'seg_list, dets_path_list length: {len(seg_list)}, {len(dets_path_list)}')

	# Aggregate objects in segments
	

if __name__ == '__main__':
	main()