import sys, os, numpy as np, pandas as pd, json, torch
from tqdm import tqdm

def main():
	# Args
	output_network_path = sys.argv[1]
	freq_dict_path = sys.argv[2]
	label_map_path = sys.argv[3]
	# label_map_path = 'label_map_55-od_2_100.json'
	# output_network_path = 'output_network/trn_rgb-val.pt'
	# freq_dict_path = 'output_val_freq/output_val_freq-0.5.json'

	# Opens stuff
	label_map = json.load(open(label_map_path))
	output_network = torch.load(output_network_path)
	freq_dict = json.load(open(freq_dict_path))
	# print(label_map)
	# print(output_network[0])
	# print(output_network[0].keys())
	# print(len(output_network))

	# Goes through the segments
	output_new = []
	for seg in tqdm(output_network):
		# Pulls dets from network
		verb_output = seg['verb_output']
		noun_output = seg['noun_output']
		narration_id = seg['narration_id']
		video_id = seg['video_id']

		# Gets object detection frequency list and converts
		freq_list = []
		freq_total = 0
		for obj_list in freq_dict[narration_id]:
			# print(obj_list)
			class_od = obj_list[1]
			class_100 = label_map[str(class_od)]
			freq = obj_list[2]
			freq_list.append([class_100, freq])
			freq_total += freq

		# Sorts by freq
		sorted(freq_list, key=lambda x: x[1])

		# Fill in noun list
		for val, freq in freq_list:
			perc = freq / freq_total

			if val != -1:
				noun_output[val] = perc

		# Creates new dict
		temp_dict = {
			'verb_output' : verb_output,
			'noun_output' : noun_output,
			'narration_id' : narration_id,
			'video_id' : video_id
		}

		# Adds to lislt
		output_new.append(temp_dict)

		# print(noun_output)
		# print(len(noun_output))
		# print(narration_id)
		# print(video_id)
		# sys.exit()
		# break

	# Saves
	out_path = output_network_path.replace('.pt', '-converted.pt')
	torch.save(output_new, out_path)

if __name__ == '__main__':
	main()