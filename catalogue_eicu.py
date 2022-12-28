#!/usr/bin/python3
import pandas as pd
import os
import json

BASE_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(BASE_DIR, '../physionet.org/files/eicu-crd/2.0/')
OUTPUT_PATH_DICT = os.path.join(BASE_DIR, './catalogue_eicu.json')
OUTPUT_PATH_IGNORED = os.path.join(BASE_DIR, './catalogue_eicu_ignored.txt')


# collect csv file paths
input_file_paths = []
for file_name in os.listdir(INPUT_DIR):
    if file_name.endswith('.csv.gz'):
        input_file_paths.append(
            os.path.join(INPUT_DIR, file_name)
        )


# read csv files and extract catalogue dict
ignored_columns = set()
result_dict = {}
for input_file_path in input_file_paths:
    df = pd.read_csv(input_file_path, header=0, nrows=1)
    for column_name in df.columns:
        if column_name in ignored_columns:
            continue
        elif column_name in result_dict:
            # ignore columns that appear in multiple tables
            del result_dict[column_name]
            ignored_columns.add(column_name)
            continue
        else:
            result_dict[column_name] = input_file_path


# manual fix


def specify_manually(column_name, path):
    result_dict[column_name] = os.path.join(INPUT_DIR, path)
    ignored_columns.discard(column_name)


specify_manually('gender', 'patient.csv.gz')
specify_manually('age', 'patient.csv.gz')


# output result dict
with open(OUTPUT_PATH_DICT, 'w') as output_file:
    json.dump(
        result_dict,
        output_file,
        indent=2,
    )


# output ignored columns
with open(OUTPUT_PATH_IGNORED, 'w') as output_file:
    for ignored_column in ignored_columns:
        output_file.write(f'{ignored_column}\n')


# success
print('Done.')
