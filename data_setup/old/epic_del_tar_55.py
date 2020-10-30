import re, os, sys, subprocess

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

def find_tars(base_dir, reg_str):
	# Creates regex
	reg = re.compile(reg_str)

	# Searches for files
	epic_tup = find_reg(base_dir, reg)

	return epic_tup 

def del_tars(tar_paths):
	for path in tar_paths:
		# Deletes tars
		print(f'tar: {path}', end='... ')
		cmd_list = ['rm', path]
		subprocess.run(cmd_list)
		print('Done.\n')
	
	return True

def main():
	# Argument for base directories to search
	base_dir = sys.argv[1]  # epic-data dir

	# Find tar files
	reg_str = r'^P\d\d_\d\d.tar$'
	tar_paths, tar_files = find_tars(base_dir, reg_str)
	tar_paths.sort()

	# Copy tars
	del_tars(tar_paths)

if __name__ == '__main__':
	main()