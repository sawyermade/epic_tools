import os, sys, gulpio, re, collections, json, time

def read_gulp(gulp_dir):
	# Read gulp directory
	gd = gulpio.GulpDirectory(gulp_dir)

	# Get list of segments from meta data and 3 value stable sort
	reg = r'^P([0-9]+)_([0-9]+)_([0-9]+)$'
	match_list = sorted(
		[re.match(reg, s) for s in gd.chunk_lookup.keys()], 
		key=lambda x: (int(x.group(1)), int(x.group(2)), int(x.group(3)))
	)
	seg_list = [s.group(0) for s in match_list]
	
	# Return segment id list and gulp directory
	return (gd, seg_list)

def get_times(gd, seg_list):
	# Loop through segments
	time_list = []
	num_segs = len(seg_list)
	print(f'Segment count: 0 of {num_segs}')
	for seg, c in zip(seg_list, range(len(seg_list))):
		if (c+1) % 100 == 0: print(f'Segment count: {c+1} of {num_segs}')
		meta = gd[seg][1]
		start, stop = int(meta['start_frame']), int(meta['stop_frame'])
		total = (stop - start + 1) / 50.0
		time_list.append(total)

	# Returns time list
	print(f'Segment count: {num_segs} of {num_segs}')
	return time_list

def get_time_metrics(time_list):
	# Loop through times
	min_time, max_time = 0, -1
	for t in time_list:
		if min_time > max_time:
			min_time, max_time = t, t
		elif t < min_time:
			min_time = t
		elif t > max_time:
			max_time = t

	# Get avg time
	avg_time = sum(time_list) / len(time_list)

	# Return metrics
	return (min_time, max_time, avg_time)

def main():
	# Timer
	time_start = time.perf_counter()

	# Args
	gulp_dir = sys.argv[1]

	# Read gulp dir
	print(f'Reading gulp directory: {gulp_dir}')
	gd, seg_list = read_gulp(gulp_dir)
	print('Done.\n')

	# Get time list of segments
	print(f'Getting time list...')
	time_list = get_times(gd, seg_list)
	print('Done.\n')

	# Get metrics min, max, and avg time for actions
	print(f'Getting time metrics...')
	min_time, max_time, avg_time = get_time_metrics(time_list)
	print('Done.\n')

	# Print metrics
	print('Metrics:')
	print(f'min, max, avg times: {min_time}, {max_time}, {avg_time}\nTime to run {len(seg_list)} segments: {time.perf_counter() - time_start}s')

	# Creates segment and time dicts
	out_dict = collections.OrderedDict()
	for s, t in zip(seg_list, time_list):
		out_dict[s] = t
	
	# Saves dict and min, max, avg
	out_dir = 'output_times'
	if not os.path.exists(out_dir): os.makedirs(out_dir)
	fname = os.path.split(gulp_dir)[-1]
	out_path = os.path.join(out_dir, fname)
	with open(out_path + '.json', 'w') as fp:
		json.dump(out_dict, fp, indent=3)
	with open(out_path + '.txt', 'w') as fp:
		fp.write(f'min, max, avg times: {min_time}, {max_time}, {avg_time}\nTime to run {len(seg_list)} segments: {time.perf_counter() - time_start}s')

if __name__ == '__main__':
	main()