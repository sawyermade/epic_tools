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

def sort_tars(tar_paths):
	# Lists needed
	rgb_test = []
	rgb_train = []
	flow_test = []
	flow_train = []

	# Finds all tars
	for path in tar_paths:
		# Split path string to find RGB or Flow
		path_split = path.split(os.sep)
		modal, tt = path_split[-4:-2]

		# Checks if RGB or Flow
		if model == 'rgb':
			if tt == 'test':
				rgb_test.append(path)

			else:
				rgb_train.append(path)

		else:
			if tt == 'test':
				flow_test.append(path)

			else:
				flow_train.append(path)
	
	# Creates tar dict
	tar_dict = {
		# RGB Dict
		'rgb' : {
			'test'  : {
				'total' : len(rgb_test),
				'list'  : rgb_test
			},

			'train' : {
				'total' : len(rgb_train),
				'list'  : rgb_train
			},

			'total' : len(rgb_test) + len(rgb_train)
		},

		# Flow dict
		'flow' : {
			'test'  : {
				'total' : len(flow_test),
				'list'  : flow_test
			},

			'train' : {
				'total' : len(flow_train),
				'list'  : flow_train
			},

			'total' : len(flow_test) + len(flow_train)
		},

		# Total tars for rgb and flow
		'total' : len(rgb_test) + len(rgb_train) + len(flow_test) + len(flow_train)
	}

	return tar_dict

def print_tar_stats(tar_dict):
	# Gets stats for rgb and flow
	num_rgb_test = tar_dict['rgb']['test']['total']
	num_rgb_train = tar_dict['rgb']['train']['total']
	num_rgb = tar_dict['rgb']['total']
	num_flow_test = tar_dict['flow']['test']['total']
	num_flow_train = tar_dict['flow']['train']['total']
	num_flow = tar_dict['flow']['total']
	num_total = tar_dict['total']

	# Prints info
	print('\nRGB INFO:\n')
	print(f'RGB Test: {num_rgb_test}')
	print(f'RGB Train: {num_rgb_train}')
	print(f'RGB Total: {num_rgb}\n')

	print('\nFLOW INFO:\n')
	print(f'Flow Test: {num_flow_test}')
	print(f'Flow Train: {num_flow_train}')
	print(f'Flow Total: {num_flow}\n')

def main():
	# Argument for base directories to search
	base_dir = sys.argv[1]  # 3h91syskeag572hl6tvuovwv4d/frames_rgb_flow

	# Find tar files
	reg_str = r'^P\d\d_\d\d.tar$'
	tar_paths, tar_files = find_tars(base_dir, reg_str)
	tar_paths.sort()

	# Copy tars
	tar_dict = sort_tars(tar_paths)

	# Gets tar stats
	print_tar_stats(tar_dict)

if __name__ == '__main__':
	main()