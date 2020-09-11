import re, os, sys

def find_reg(base_dir, reg):
	# Walks through directories finding matching tars for regex
	paths = []
	all_files = []
	for root, dirs, files in os.walk(base_dir):
		if files:
			# Finds all matching tar files in directory
			files_match = [f for f in files if reg.match(f)]
			paths += [os.path.join(root, f) for f in files_match]
			all_files += files_match

	return (paths, all_files)

def find_mp4s(base_dir_55, base_dir_100):
	# Creates regex
	reg_str_55 = r'^P\d\d_\d\d.MP4$'
	reg_str_100 = r'^P\d\d_\d\d\d.MP4$'
	reg_55 = re.compile(reg_str_55)
	reg_100 = re.compile(reg_str_100)

	# Searches for files
	epic_55_tup = find_reg(base_dir_55, reg_55)
	epic_100_tup = find_reg(base_dir_100, reg_100)

	return epic_55_tup, epic_100_tup

def find_tars(base_dir_55, base_dir_100):
	# Creates regex
	reg_str_55 = r'^P\d\d_\d\d.tar$'
	reg_str_100 = r'^P\d\d_\d\d\d.tar$'
	reg_55 = re.compile(reg_str_55)
	reg_100 = re.compile(reg_str_100)

	# Searches for files
	epic_55_tup = find_reg(base_dir_55, reg_55)
	epic_100_tup = find_reg(base_dir_100, reg_100)

	return epic_55_tup, epic_100_tup

def extract_tars(paths):
	for path in paths:
		# Gets dir and filename
		file_dir = f'{os.sep}'.join(path.split(os.sep)[:-1])
		file_name = path.split(os.sep)[-1].split('.')[0]

		# Creates new directory
		new_dir = os.path.join(file_dir, file_name)
		if not os.path.exists(new_dir):
			os.makedirs(new_dir)

		# Extract tars to new directory
		os.system(f'tar xf {path} -C {new_dir}')
		# return None

	return True
	
def main():
	# Argument for base directory to search
	base_dir_55 = sys.argv[1]  # 3h91syskeag572hl6tvuovwv4d
	base_dir_100 = sys.argv[2] # 2g1n6qdydwa9u22shpxqzp0t8m

	# Find all tar files
	tar_epic_55, tar_epic_100 = find_tars(base_dir_55, base_dir_100)
	tar_paths_55, tar_files_55 = tar_epic_55 
	tar_paths_100, tar_files_100 = tar_epic_100 
	print(f'num epic 55 tar files = {len(tar_paths_55)}')
	print(f'num epic 100 tar files = {len(tar_paths_100)}')

	# Find all mp4 files
	mp4_epic_55, mp4_epic_100 = find_mp4s(base_dir_55, base_dir_100)
	mp4_paths_55, mp4_files_55 = mp4_epic_55
	mp4_paths_100, mp4_files_100 = mp4_epic_100
	print(f'num epic 55 mp4 files = {len(mp4_paths_55)}')
	print(f'num epic 100 mp4 files = {len(mp4_paths_100)}')

	# Sorts and finds missing for epic 55
	tar_files_55 = [f.split('.')[0] for f in tar_files_55]
	mp4_files_55 = [f.split('.')[0] for f in mp4_files_55]
	tar_files_55.sort()
	mp4_files_55.sort()
	missing_files_55 = [f for f in tar_files_55 if f not in mp4_files_55]
	print(f'missing epic 55 videos:\n {missing_files_55}')

	# Sorts and finds missing for epic 100
	tar_files_100 = [f.split('.')[0] for f in tar_files_100]
	mp4_files_100 = [f.split('.')[0] for f in mp4_files_100]
	tar_files_100.sort()
	mp4_files_100.sort()
	missing_files_100 = [f for f in tar_files_100 if f not in mp4_files_100]
	print(f'missing epic 100 videos:\n {missing_files_100}')

	# Extract tars
	tar_paths_55.sort()
	tar_paths_100.sort()
	extract_tars(tar_paths_55)
	extract_tars(tar_paths_100)

if __name__ == '__main__':
	main()