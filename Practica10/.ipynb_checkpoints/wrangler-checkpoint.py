# TODO: verificar que hay las mismas entradas que en json

import json
import csv


def load_json(file_path):
    with open(file_path, "r") as input_file:
        dic = json.load(input_file)
        return dic
    
    
def load_csv(file_path):
    with open(file_path, "r") as input_file:
        reader = csv.reader(input_file, delimiter = ";")
        matrix = [row for row in reader]
    return matrix

def check_number_of_universities(universities, universities_matrix):
    """
    Checks that the number of universities in the csv and the json file is gthe same.
    
    Params
    -------
    universities : dict
        Dictionary with the data of each university
    
    universities_matrix: list
    
    Return
    -------
    check : Boolean
        True if the lenght is the same, false otherwise.
    """
    if len(universities) == len(universities_matrix):
        print("The json and the csv have the same number of universities")
        return True
    else:
        print("The json and the csv have the same number of universities")
        return False
    
def get_unique_keys(universities):
    """
    Returns the unique keys for all the university items in the json file.
    
    Params
    -------
    universities : dict
        Dictionary with the data of each university
        
    Return
    -------
    unique_keys : list
        Unique keys for the all university items in the json file.
    """
    keys = []
    for university, data in universities.items():
        for key in data:
            keys.append(key)
    unique_keys = list(set(keys))
    return unique_keys




file_path = r"universities.json"
universities = load_json(file_path)

file_path = r"universities.csv"
universities_matrix = load_csv(file_path)

check_number_of_universities(universities, universities_matrix)
unique_keys = get_unique_keys(universities)

print("----- Unique Keys -----")
for key in unique_keys:
    print(key)

            