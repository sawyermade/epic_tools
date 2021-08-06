import sys, os, numpy as np, time, gulpio2 as gulpio, compress_json, re, json, time
from tqdm import tqdm

def main():
	# Args 
	freq_path = sys.argv[1]

	# Open freq json
	with open(freq_path) as fp:
		freq_dict = json.load(fp)

	# Validation ground truth
	with open('epic_100_gt-val.json') as fp:
		gt_dict = json.load(fp)

	# Sorted seg keys
	# Get list of segments from meta data and 3 value/level stable sort
	# reg = r'^P([0-9]+)_([0-9]+)_([0-9]+)$'
	# match_list = sorted(
	# 	[re.match(reg, s) for s in gt_dict.keys()], 
	# 	key=lambda x: (int(x.group(1)), int(x.group(2)), int(x.group(3)))
	# )
	# seg_list = [s.group(0) for s in match_list]
	seg_list = sorted(gt_dict.keys())
	# print(seg_list_diff_sort)
	# sys.exit()

	# Compares top 1,3,5 freq to gt
	top_1, top_3, top_5 = 0, 0, 0
	for seg in seg_list:
		# Get dets and gt for segment
		noun_dets = freq_dict[seg]
		if noun_dets:
			noun_dets = np.asarray(noun_dets)
		noun_gt = gt_dict[seg]['noun']
		
		# Check if top 1, 3, 5 exist and slice
		if len(noun_dets) > 0: 
			noun_dets_1 = noun_dets[0, 0]
		else:
			noun_dets_1 = None

		if len(noun_dets) >= 3: 
			noun_dets_3 = noun_dets[:3, 0].tolist()
		else:
			noun_dets_3 = None

		if len(noun_dets) >= 5: 
			noun_dets_5 = noun_dets[:5, 0].tolist()
		else:
			noun_dets_5 = None

		# if noun_dets_3: print(noun_dets_3)

		# try:
		# 	noun_dets_all = noun_dets[:, 0]
		# 	# print(noun_dets_all)
		# except:
		# 	print(seg, noun_dets)

		# Split noun gt by : if present
		if ':' in noun_gt:
			noun_gt_list = noun_gt.split(':')
		else:
			noun_gt_list = [noun_gt]
		# noun_gt_list = [noun_gt]

		# Top 1
		if noun_dets_1:
			for nd in noun_dets_1:
				if nd in noun_gt_list:				
					top_1 += 1
					# print(noun_dets_1, noun_gt_list)
					break
				# else:
				# 	print(noun_dets_1, noun_gt_list)

		# Top 3
		if noun_dets_3:
			for nds in noun_dets_3:
				for nd in nds:
					if nd in noun_gt_list:
						top_3 += 1
						# print(noun_dets_3, noun_gt_list)
						break

		# Top 5
		if noun_dets_5:
			for nds in noun_dets_5:
				for nd in nds:
					if nd in noun_gt_list:
						top_5 += 1
						# print(noun_dets_5, noun_gt_list)
						break

	print(f'\ntop_1: {top_1}')
	print(f'top_3: {top_3}')
	print(f'top_5: {top_5}')


if __name__ == '__main__':
	main()