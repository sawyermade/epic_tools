import os, sys, json, re

def map_to_json(label_map_path, output_path='label_map.json'):
	# Open, read, and convert to json
	label_dict = {}
	with open(label_map_path) as fp:
		for line in fp:
			if 'id:' in line and 'liquid:' not in line:
				cid = int(line.replace('id:', ''))
				label_dict[cid] = []
				# print(f'cid: {cid}', end=', ')

			elif 'name:' in line:
				names = line.replace('name:', '').strip().strip('\'')
				# names_list = names.split(':')
				# label_dict[cid] = names_list
				label_dict[cid] = names
				# print(f'names: {names_list}')

	# Write json
	with open(output_path, 'w') as fp:
		json.dump(label_dict, fp, indent=3)

def main():
	# Path to label map
	label_map_path = 'models/EPICKitchens_FasterRCNN_label_map.pbtxt'

	# Convert to json
	map_to_json(label_map_path)

if __name__ == '__main__':
	main()