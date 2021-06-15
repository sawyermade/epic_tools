import csv, json, os, sys

def open_epic_csv(path_to_csv):
	# Open csv and read it
	with open(path_to_csv) as fp:
		for row in csv.reader(fp):
			all_noun = row[13]
			all_noun_nom = row[14]
			print(all_noun[0])
			print(all_noun_nom)
			print(f'{type(all_noun)}')
			print(f'{type(all_noun_nom)}')
			print()

	return None

def main():
	# Args
	path_to_csv = sys.argv[1]
	output_json = sys.argv[2]

	# Open csv
	gt_dict = open_epic_csv(path_to_csv)

if __name__ == '__main__':
	main()