import json, os, sys

def main():
	# Args
	input_file = sys.argv[1]

	# Load json
	with open(input_file) as fp:
		time_dict = json.load(fp)

	# Count frames
	time_list = [time_dict[key] for key in time_dict.keys()]
	time_total = sum(time_list)
	frame_count = round(time_total * 50)
	print(f'total time: {time_total}')
	print(f'total frames: {frame_count}')

if __name__ == '__main__':
	main()