import re, os, sys, subprocess, time

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

def move_tars_55(tar_paths, base_dir):
	# Create base dir if doesnt exist
	if not os.path.exists(base_dir):
		os.makedirs(base_dir)

	for path in tar_paths:
		# Gets filename and participant
		file_name = path.split(os.sep)[-1].split('.')[0]
		part_name = file_name.split('_')[0]
		rgb_flow = path.split(os.sep)[-4]

		if rgb_flow != 'rgb' and rgb_flow != 'flow':
			print(f'\nERROR: No rgb or flow in {path}\n')
			sys.exit(0)

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

def move_tars_100(tar_paths, base_dir):
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
		elif rgb_flow == 'flow_frames':
			rgb_flow = 'flow'
		else:
			print(f'\nERROR: No rgb or flow in {path}\n')
			sys.exit(0)

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
	# Timer
	time_start = time.time()

	# dir containing 3h91syskeag572hl6tvuovwv4d & 2g1n6qdydwa9u22shpxqzp0t8m dirs
	base_dir_input = sys.argv[1] 

	# Where to move to 
	base_dir_output = sys.argv[2]

	# Creates dir paths
	base_dir_input_55 = os.path.join(base_dir_input, '3h91syskeag572hl6tvuovwv4d')
	base_dir_input_100 = os.path.join(base_dir_input, '2g1n6qdydwa9u22shpxqzp0t8m')

	# Find & move epic 55 tars
	reg_str_55 = r'^P\d\d_\d\d.tar$'
	tar_paths_55, _ = find_tars(base_dir_input_55, reg_str_55)
	tar_paths_55.sort()
	

	# Finds & move epic 100 tars
	reg_str_100 = r'^P\d\d_\d\d\d.tar$'
	tar_paths_100, _ = find_tars(base_dir_input_100, reg_str_100)
	tar_paths_100.sort()

	# Moves tars
	move_tars_55(tar_paths_55, base_dir_output)
	move_tars_100(tar_paths_100, base_dir_output)

	# Writes tar counts and time
	time_end = time.time()
	time_total = time_end - time_start
	with open('output_epic_move_tar_all.txt', 'w') as of:
		of.write(f'epic 55 tar count   : {len(tar_paths_55)}\n')
		of.write(f'epic 100 tar count  : {len(tar_paths_100)}\n')
		of.write(f'epic total tar count: {len(tar_paths_100) + len(tar_paths_55)}\n')
		of.write(f'execution time      : {time_total} seconds\n')

if __name__ == '__main__':
	main()