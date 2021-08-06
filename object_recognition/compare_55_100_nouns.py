import sys, os, numpy as np, pandas as pd, json

def main():
	# Args
	# epic_55_nouns_path = sys.argv[1]
	# epic_100_nouns_path = sys.argv[2]
	# epic_55_label_map_path = sys.argv[3]
	epic_55_nouns_path = 'EPIC_55_noun_classes.csv'
	epic_100_nouns_path = 'EPIC_100_noun_classes.csv'
	epic_55_label_map_path = 'label_map.json'

	# Open csv
	epic_55_df = pd.read_csv(epic_55_nouns_path, converters={'nouns': eval})
	epic_100_df = pd.read_csv(epic_100_nouns_path, converters={'instances': eval})

	# Pull columns needed
	epic_55_classes = epic_55_df['class_key'].to_numpy()
	epic_55_instances = epic_55_df['nouns'].to_list()
	epic_100_classes = epic_100_df['key'].to_numpy()
	epic_100_instances = epic_100_df['instances'].to_list()
	print(f'epic 55 classes: {epic_55_classes.shape[0]}')
	print(f'epic 100 classes: {epic_100_classes.shape[0]}')
	
	# Go through epic 55 and 100
	class_similarity_count = 0
	class_sim_list = []
	for i in range(epic_55_classes.shape[0]):
		# Get epic 55 class and instance
		ep55_class = epic_55_classes[i]
		ep55_instance = epic_55_instances[i]

		# Compare againsta epic 100
		for j in range(epic_100_classes.shape[0]):
			# Get epic 100 class and instance
			ep100_class = epic_100_classes[j]
			ep100_instance = epic_100_instances[j]

			# Compare the two to see if 55 exists in 100
			if ep55_class == ep100_class:
				class_similarity_count += 1
				class_sim_list.append([i, ep55_class, j, ep100_class])
				# print(f'ep55_class, ep100_class: {ep55_class}, {ep100_class}')
				break

			elif ep55_class in ep100_instance:
				class_similarity_count += 1
				class_sim_list.append([i, ep55_class, j, ep100_class])
				# print(f'ep55_class, ep100_instance: {ep55_class}, {ep100_instance}')
				break

			# else:
			# 	for inst in ep55_instance:
			# 		if inst in ep100_instance:
			# 			class_similarity_count += 1
			# 			break

	# Tests
	class_sim_list_100 = sorted(class_sim_list, key=lambda x: x[2])
	class_count_100 = [0] * 300
	for c in class_sim_list_100: class_count_100[c[2]] += 1
	print(f'class_similarity_count: {class_similarity_count}')
	print(f'class_sim_list: {class_sim_list}\n')
	print(f'class_sim_list_100: {class_sim_list_100}\n')
	print(f'class_count_100: {class_count_100}\n')

	# Check for epic 55 doubles
	match_list_55 = [0] * 352
	for match in class_sim_list:
		match_list_55[match[0]] += 1
	match_list_55_missing = np.where(np.asarray(match_list_55) == 0)[0]
	print(f'epic 55 match list: {match_list_55}\n')
	print(f'epic 55 missing: {len(match_list_55_missing)}, {match_list_55_missing}\n')

	# Check for epic 100 doubles
	match_list_100 = [0] * 300
	for match in class_sim_list:
		match_list_100[match[2]] += 1
	match_list_100_missing = list(np.where(np.asarray(match_list_100) == 0))[0]
	print(f'epic 100 match list: {match_list_100}\n')
	print(f'epic 100 missing: {len(match_list_100_missing)}, {match_list_100_missing}\n')

	# Print missing epic 55 classes
	ep55_missing_labels = []
	for c in match_list_55_missing:
		ep55_missing_labels.append(epic_55_classes[c])
	print(f'ep55 missing labels: {ep55_missing_labels}\n')

	# Print missing epic 100 classes
	ep100_missing_labels = []
	for c in match_list_100_missing:
		ep100_missing_labels.append(epic_100_classes[c])
	print(f'ep100 missing labels: {ep100_missing_labels}\n')

	# Compare epic 55 label map vs epic 55 nouns
	count = 0
	pop_list = []
	ep55_label_map = json.load(open('label_map.json'))
	for k, c in ep55_label_map.items():
		if c in epic_55_classes:
			count += 1
			cm = np.where(epic_55_classes == c)[0]
			pop_list.append((int(k), cm[0]))
			# print(c)
	
	print(f'count: {count}\n')
	print(f'pop_list: {len(pop_list)}, {pop_list}\n')

	obj_nouns = list(ep55_label_map.values())
	# print(obj_nouns)
	miss_list = []
	for i in range(len(epic_55_classes)):
		n = epic_55_classes[i]
		if n not in obj_nouns:
			miss_list.append(n)
	print(f'miss_list: {miss_list}\n')

	# Make mapping vector
	class_map_100 = [[0]] * 300
	for c in class_sim_list_100:
		c55 = c[0]
		c100 = c[2]
		if class_map_100[c100][0] == 0:
			class_map_100[c100] = [c55]
		else:
			class_map_100[c100].append(c55) 
	print(f'class_map_100: {class_map_100}\n')

	class_map_55 = [[-1]] * 352
	for c in class_sim_list:
		c55 = c[0]
		c100 = c[2]
		if class_map_55[c55][0] == -1:
			class_map_55[c55] = [c100]
		else:
			class_map_55[c55].append(c100)
	map_55_count = [len(c) for c in class_map_55]
	print(f'class_map_55: {len(class_map_55)}\n{class_map_55}\n')
	print(f'map_55_count: {max(map_55_count)}\n{map_55_count}\n')

	# Maps epic 55 nouns to object detector nominal values
	epic_55_label_map = json.load(open(epic_55_label_map_path))
	epic_55_keys = [int(k) for k in epic_55_label_map.keys()]
	epic_55_keys.sort()
	# print(epic_55_keys)
	# print(len(epic_55_keys))
	# print(epic_55_classes)
	# epic_55_label_map_vector = [int(l) for k, l in epic_]

	epic_55_od2gt = []
	epic_55_od2gt_missed = []
	for key in epic_55_keys:
		label_od = epic_55_label_map[str(key)]
		
		flag = True
		for i, label_gt in enumerate(epic_55_classes):
			if label_od == label_gt:
				epic_55_od2gt.append([key, i])
				flag = False
		if flag:
			epic_55_od2gt_missed.append(key)

	epic_55_od2gt_dict = {c[0] : c[1] for c in epic_55_od2gt}
	# json.dump(epic_55_od2gt_dict, open('label_map_55-od2gt.json', 'w'), indent=3)

	print(f'epic_55_od2gt_missed: {epic_55_od2gt_missed}\n')
	print(f'epic_55_od2gt: {len(epic_55_od2gt)}\n{epic_55_od2gt}\n')
	print(f'epic_55_od2gt_dict: {epic_55_od2gt_dict}\n')


	# Maps object detector to epic 100
	map_od_to_100 = [-1] * 291
	for c in epic_55_od2gt:
		c_od = c[0]
		c_55 = c[1]
		c_100 = class_map_55[c_55][0]

		map_od_to_100[c_od] = c_100

	count = 0
	for c in map_od_to_100: 
		if c == -1: count += 1
	print(map_od_to_100, end='\n\n')
	print(count)
	print(len(map_od_to_100))

	od_to_100_dict = {}
	for i in range(1, 291):
		c_od = i
		c_100 = map_od_to_100[i]

		od_to_100_dict[c_od] = c_100
	# print(od_to_100_dict)
	# json.dump(od_to_100_dict, open('label_map_55-od_2_100.json', 'w'), indent=3)


if __name__ == '__main__':
	main()