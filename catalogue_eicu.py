#!/usr/bin/env python3
import pandas as pd
import os
import json
from common_eicu import *

OUTPUT_PATH_SINGLE = relative_path('catalogue_eicu_single.json')
OUTPUT_PATH_MULTIPLE = relative_path('catalogue_eicu_multiple.json')

# collect csv file paths
input_file_paths = []
for file_name in os.listdir(EICU_DIR):
    if file_name.endswith('.csv.gz'):
        input_file_paths.append(
            os.path.join(EICU_DIR, file_name)
        )

# read csv files and extract catalogue dict
single_dict = {}  # column_name -> path
multiple_dict = {}  # column_name -> [paths...]
for input_file_path in input_file_paths:
    df = pd.read_csv(input_file_path, header=0, nrows=1)
    for column_name in df.columns:
        if column_name in multiple_dict:
            multiple_dict[column_name].append(input_file_path)
        elif column_name in single_dict:
            multiple_dict[column_name] = [
                single_dict[column_name],
                input_file_path,
            ]
            del single_dict[column_name]
        else:
            single_dict[column_name] = input_file_path

# manual fix
single_dict.update(
    gender=eicu_path('patient.csv.gz'),
    age=eicu_path('patient.csv.gz'),
)

# output result dict
with open(OUTPUT_PATH_SINGLE, 'w') as output_file:
    json.dump(
        single_dict,
        output_file,
        indent=2,
    )

# output ignored columns
with open(OUTPUT_PATH_MULTIPLE, 'w') as output_file:
    json.dump(
        multiple_dict,
        output_file,
        indent=2,
    )

# success
print('Done.')
