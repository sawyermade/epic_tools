# pip install gulpio
import os, sys, gulpio, re
from PIL import Image

def read_gulp(gulp_dir):
	# Read gulp directory
	gd = gulpio.GulpDirectory(gulp_dir)

	# Get list of segments from meta data and 3 value stable sort
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

	# Read gulp dir
	gd, seg_list = read_gulp(gulp_dir)
	print(f'seg_list len: {len(seg_list)}')

	# View frames
	frames, meta = gd[seg_list[0]]
	print(f'frames, meta len: {len(frames)}, {len(meta)}')
	print(f'meta dict: \n{meta}')
	print(f'frames type: {type(frames[0])}')
	Image.fromarray(frames[0]).show()

if __name__ == '__main__':
	main()