import json, os, sys, gulpio2 as gulpio, re
from tqdm import tqdm

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
	output_path = sys.argv[2]

	# Open csv
	gd, seg_list = read_gulp(gulp_dir)

	# Goes through meta
	gt_dict = {}
	for seg in tqdm(seg_list):
		_, meta = gd[seg]
		verb = meta['verb']
		verb_class = meta['verb_class']
		noun = meta['noun']
		noun_class = meta['noun_class']
		
		gt_dict[seg] = {
			'verb' : verb,
			'verb_class' : int(verb_class),
			'noun' : noun,
			'noun_class' : int(noun_class)
		}

	# writes json
	with open(output_path, 'w') as fp:
		json.dump(gt_dict, fp, indent=3)

if __name__ == '__main__':
	main()