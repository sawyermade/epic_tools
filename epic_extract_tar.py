import re, os, sys

def find_mp4s(base_dir):
	# Creates regex
	reg_str = r'^P\d\d_\d\d.MP4$'
	reg = re.compile(reg_str)

	# Walks through directories finding matching tars
	mp4_paths = []
	mp4_all_files = []
	for root, dirs, files in os.walk(base_dir):
		if files:
			# Finds all matching tar files in directory
			mp4_files = [f for f in files if reg.match(f)]
			mp4_all_files += mp4_files
			mp4_paths += [os.path.join(root, f) for f in mp4_files]

	return mp4_paths, mp4_all_files

def find_tars(base_dir):
	# Creates regex
	reg_str = r'^P\d\d_\d\d.tar$'
	reg = re.compile(reg_str)

	# Walks through directories finding matching tars
	tar_paths = []
	tar_all_files = []
	for root, dirs, files in os.walk(base_dir):
		if files:
			# Finds all matching tar files in directory
			tar_files = [f for f in files if reg.match(f)]
			tar_all_files += tar_files
			tar_paths += [os.path.join(root, f) for f in tar_files]

	return tar_paths, tar_all_files
	
def main():
	# Argument for base directory to search
	base_dir = sys.argv[1]
	if len(sys.argv) > 2: mp4_dir = sys.argv[2]

	# Find all tar files
	tar_paths, tar_files = find_tars(base_dir)
	# print(tar_paths)
	print(f'num tar files = {len(tar_paths)}')

	mp4_paths, mp4_files = find_mp4s(mp4_dir)
	print(f'num mp4 files = {len(mp4_paths)}')

	tar_files = [f.split('.')[0] for f in tar_files]
	mp4_files = [f.split('.')[0] for f in mp4_files]
	tar_files.sort()
	mp4_files.sort()

	missing_files = [f for f in tar_files if f not in mp4_files]
	print(missing_files)

if __name__ == '__main__':
	main()