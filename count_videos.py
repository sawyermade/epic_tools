import re, os, sys

def find_reg(base_dir, reg):
	# Walks through directories finding all matching files for regex
	paths = []
	all_files = []
	if base_dir is not None:
		for root, dirs, files in os.walk(base_dir):
			if files:
				# Finds all matching files in directory
				files_match = [f for f in files if reg.match(f)]
				paths += [os.path.join(root, f) for f in files_match]
				all_files += files_match

	return (paths, all_files)

def main():
	# Base dir
	base_dir = sys.argv[1]

	# Finds videos for epic 55
	reg_str_55 = r'^P\d\d_\d\d.MP4$'
	reg_55 = re.compile(reg_str_55)
	_, mp4_files = find_reg(base_dir, reg_55)

	print(f'\nNumber of MP4 Files in {base_dir}: {len(mp4_files)}\n')

if __name__ == '__main__':
	main()