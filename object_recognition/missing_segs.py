import os, sys, gulpio, numpy as np, re, json

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

def get_missing(seg_list, seg_output_list):
	missing_segs, missing_index = [], []
	for i, seg in enumerate(seg_list):
		if not seg in seg_output_list:
			missing_segs.append(seg)
			missing_index.append(i)

	return missing_segs, missing_index

def main():
	# Path
	gulp_dir = sys.argv[1]
	output_path = sys.argv[2]

	# Get gulped seg_list
	_, seg_list = read_gulp(gulp_dir)

	# Get dir list
	dir_list = os.listdir(output_path)
	seg_output_list = [f.replace('.json.bz', '') for f in dir_list]

	# Get missing segs and seg numbers
	missing_segs, missing_index = get_missing(seg_list, seg_output_list)
	# print(missing_index)
	print(f'\nnum missing: {len(missing_index)}')
	if len(missing_index) == 0:
		print('Nothing missing.')
	else:
		print(f'min, max: {min(missing_index)}, {max(missing_index)}')

	# Save dict
	# missing_dict = {
	# 	'missing_segs' : missing_segs,
	# 	'missing_index' : missing_index
	# }
	# with open('missing.json', 'w') as fp:
	# 	json.dump(missing_dict, fp, indent=3)

if __name__ == '__main__':
	main()