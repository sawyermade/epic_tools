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

def copy_tars(tar_paths, base_dir):
	# Create base dir if doesnt exist
	if not os.path.exists(base_dir):
		os.makedirs(base_dir)

	for path in tar_paths:
		# Gets filename and participant
		file_name = path.split(os.sep)[-1].split('.')[0]
		part_name = file_name.split('_')[0]
		rgb_flow = path.split(os.sep)[-2]

		if rgb_flow == 'rgb_frames':
			rgb_flow = 'rgb'
		else:
			rgb_flow = 'flow'

		# Creates new directory
		new_dir = os.path.join(base_dir, rgb_flow, part_name)
		print(f'tar: {path}')
		print(f'moving to: {new_dir}')
		if not os.path.exists(new_dir):
			os.makedirs(new_dir)

		# Extract tars to new directory
		cmd_list = ['mv', path, new_dir]
		subprocess.run(cmd_list)
		print('Done.\n')
	
	return True

def main():
	# Argument for base directories to search
	base_dir_input = sys.argv[1]  # 2g1n6qdydwa9u22shpxqzp0t8m
	base_dir_output = sys.argv[2] # Where to copy to

	# Find tar files
	reg_str = r'^P\d\d_\d\d\d.tar$'
	tar_paths, tar_files = find_tars(base_dir_input, reg_str)
	tar_paths.sort()

	# Copy tars
	copy_tars(tar_paths, base_dir_output)

if __name__ == '__main__':
	main()