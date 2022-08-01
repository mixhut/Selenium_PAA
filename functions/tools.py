import pickle
import json
import os
# import sys
from os.path import exists


def save_pickle(name, data):
	with open(name, 'wb') as f:
		pickle.dump(data, f)


def load_pickle(name):
	with open(name, 'rb') as f:
		return pickle.load(f)


def pickle_it(file, new_data):
	# Check if pickle file already exists, if not make new file
	pickle_exists = exists(file)
	if pickle_exists is True:
		data = load_pickle(file)
		data.append(new_data)
		save_pickle(file, data)
	else:
		save_pickle(file, new_data)


def pickle2json(file):
	# open pickle file
	with open(file, 'rb') as file_in:
		obj = pickle.load(file_in)
	# convert pickle object to json object
	json_obj = json.loads(json.dumps(obj, default=str))
	# write the json file
	with open(os.path.splitext(file)[0] + '.json', 'w', encoding='utf-8') as file_out:
		json.dump(json_obj, file_out, ensure_ascii=False, indent=4)


def cp_load(file):
	checkpoint_exists = exists(file)
	if checkpoint_exists is True:
		with open(file, 'r', encoding='utf-8') as f:
			check = int(f.readline())
			print('Checkpoint found:', check)
			return check
	else:
		check = int(0)
		return check


def cp_write(file, cp: int):
	with open(file, 'w', encoding='utf-8') as f:
		f.write(str(cp))
		f.close()


def save_json(file, data):
	with open(file, 'a', encoding='utf-8') as f:  # appends to json file
		json.dump(data, f, indent=4)
		f.write(',\n')


def load_json(file):
	with open(file, 'r', encoding='utf-8') as f:
		data = json.load(f)
	return data


def remove_duplicate_keys(j_data, j_key):
	unique_elements = []
	cleaned_data = []
	keys = []
	for x, j in enumerate(j_data):
		if j_data[x][j_key] not in unique_elements:
			unique_elements.append(j_data[x][j_key])
			keys.append(x)

	for key in keys:
		cleaned_data.append(j_data[key])

	return cleaned_data


# Append JSON object to output file JSON array
def append_json(file, data):
	# Check exists
	json_exists = exists(file)
	if json_exists is True:
		with open(file, 'a+', encoding='utf-8') as outfile:
			outfile.seek(0, os.SEEK_END)
			outfile.seek(outfile.tell()-1, os.SEEK_SET)
			outfile.truncate()
			outfile.write(',')
			json.dump(data, outfile, indent=4)
			outfile.write('\n]')
	else:
		# Create file
		with open(file, 'w', encoding='utf-8') as f:  # appends to json file
			f.write('[\n')
			json.dump(data, f, indent=4)
			f.write('\n')
