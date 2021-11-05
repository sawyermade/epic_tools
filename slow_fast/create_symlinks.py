import sys, os, re

def main():
	# Args
	frame_dir = sys.argv[1]
	symlink_dir = sys.argv[2]

	# Get absolute paths
	frame_dir = os.path.abspath(frame_dir)
	symlink_dir = os.path.abspath(symlink_dir)
	print(f'frame_dir, symlink_dir: {frame_dir}, {symlink_dir}')

	# Create output symlink dir if it doesnt exist
	if os.path.exists(symlink_dir):
		os.system(f'rm -rf {symlink_dir}')
	if not os.path.exists(symlink_dir):
		os.makedirs(symlink_dir)

	# Get participant dirs
	reg_str = r'^P[\d]{2}$'
	reg = re.compile(reg_str)
	part_dirs = [d for d in os.listdir(frame_dir) if reg.match(d)]
	# print(part_dirs)

	# Create full absolute dir paths
	part_paths = [os.path.join(frame_dir, d) for d in part_dirs]
	part_paths = [d for d in part_paths if os.path.isdir(d)]
	# print(part_paths)

	# Create symlinks
	reg_str = r'^P[\d]{2}_[\d]{2,3}$'
	reg = re.compile(reg_str)
	for part in part_paths:
		# Get directories in part path
		parts = os.listdir(part)
		parts = [d for d in parts if reg.match(d)]
		parts = [os.path.join(part, d) for d in parts]

		# Get participant ID
		pid = part.rsplit(os.sep, 1)[-1]

		# Create links
		symlink_final = os.path.join(symlink_dir, pid, 'rgb_frames')
		if not os.path.exists(symlink_final):
			os.makedirs(symlink_final)
		for p in parts:
			os.system(f'ln -s {p} {symlink_final}')


if __name__ == '__main__':
	main()