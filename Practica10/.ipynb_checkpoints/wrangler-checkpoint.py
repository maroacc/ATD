# TODO: verificar que hay las mismas entradas que en json

import json

def load_json(file_path):
    with open(file_path, "r") as input_file:
        dic = json.load(input_file)
        return dic

file_path = r"universities.json"
universities = load_json(file_path)

keys = []
for university, data in universities.items():
    for key in data:
        keys.append(key)

unique_keys = list(set(keys))

print("----- Unique Keys -----")
for key in unique_keys:
    print(key)

            