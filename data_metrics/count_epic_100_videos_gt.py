import sys, os

def main():
	csv_path = sys.argv[1] # Path to gt file, ex: EPIC_100_train.csv
	out_file = sys.argv[2] # output text file of your choice, ex: ./output_train.txt

	# Makes output dirs if needed
	out_split = out_file.split(os.sep)
	if len(out_split) > 1 :
		new_dir = os.path.join(out_split[:-1])
		if not os.path.exists(new_dir):
			os.makedirs(new_dir)

	vid_set = set()
	with open(csv_path) as cf:

		for line in cf:
			c_list = line.split(',')
			vid = c_list[2]
			vid_set.add(vid)

		vid_list = sorted(vid_set)[:-1]
		with open(out_file, 'w') as of:

			for vid in vid_list:
				of.write(f'{vid}\n')

			of.write(f'\nTotal Videos: {len(vid_list)}\n')


if __name__ == '__main__':
	main()