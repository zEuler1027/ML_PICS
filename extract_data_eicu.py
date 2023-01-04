#!/usr/bin/python3
from functools import reduce
import json
import pandas as pd
import numpy as np
from common_eicu import *
from math import isnan

# COMPACT_MODE = False
COMPACT_MODE = True

TEST_MODE = False
# TEST_MODE = True

# DROP_NA = 'all'
DROP_NA = 'partial'
# DROP_NA = False

# COMPRESS_OUTPUT = False
COMPRESS_OUTPUT = True

FILTERED_LAB_PATH = relative_path('lab_filtered.csv.gz')
FILTERED_EXAM_PATH = relative_path('exam_filtered.csv.gz')
FILTERED_TREATMENT_PATH = relative_path('treatment_filtered.csv.gz')

OUTPUT_PATH = relative_path(
    'data_eicu_'
    + ('compact' if COMPACT_MODE else 'full')
    + '_raw'
    + ('' if DROP_NA else '_na')
    + ('_test' if TEST_MODE else '')
    + '.csv'
    + ('.gz' if COMPRESS_OUTPUT else '')
)


def post_process_compact(df):

    def map_age(age):
        if age != age:
            return age
        elif age == '> 89':
            return 90
        else:
            return int(age)

    df['age'] = df['age'].map(map_age)

    df['vasopressor'] = df['vasopressor'].map(
        lambda v: v if v != v else int(v)
    )


def post_process_full(df):

    post_process_compact(df)

    df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
    del df['weight']
    del df['height']


# dynamically generate the map of data sources
print('Collecting data sources...')
data_sources = {}
with open(CATALOGUE_PATH, 'r') as catalogue_file:
    catalogue = json.load(catalogue_file)
    for column_name in REQUIRED_COLUMNS:
        if not column_name in catalogue:
            raise Exception(
                f'Cannot find column "{column_name}" in catalogue!'
            )
        file_path = catalogue[column_name]
        if file_path in data_sources:
            data_sources[file_path].append(column_name)
        else:
            data_sources[file_path] = [column_name]


# collect required data frames
print('Collecting required data frames...')
data_frames = []
for input_path, column_names in data_sources.items():
    usecols = [KEY_IDENTITY] + column_names
    data_frame = pd.read_csv(
        input_path,
        usecols=usecols,
        index_col=KEY_IDENTITY,
    )
    data_frame.columns = map(
        map_column_name,
        data_frame.columns,
    )
    # print(data_frame)
    # print(data_frame.dtypes)
    data_frames.append(data_frame)


# join data frames
print('Joining data frames...')
df_output = reduce(
    lambda df_0, df_1: df_0.join(df_1),
    data_frames,
)
df_output.drop_duplicates(inplace=True)
if DROP_NA != False:
    df_output.dropna(inplace=True)


# collect treatment info

print('Collecting treatment info...')

if TEST_MODE:
    df_treatment = pd.read_csv(
        FILTERED_TREATMENT_PATH,
        usecols=[KEY_IDENTITY, KEY_TREATMENT_STRING],
        nrows=TEST_ROWS,  # for quick test
    )
else:
    df_treatment = pd.read_csv(
        FILTERED_TREATMENT_PATH,
        usecols=[KEY_IDENTITY, KEY_TREATMENT_STRING],
    )

treatment_record_count = len(df_treatment)

for keyword in REQUIRED_TREATMENT_KEYWORDS:
    column_name = map_column_name(keyword)
    df_output[column_name] = False  # init

for treatment_index in df_treatment.index:

    print(
        f'\tProcessing treatment record {treatment_index + 1:7}/{treatment_record_count}'
    )
    treatment_record = df_treatment.iloc[treatment_index]

    identity = treatment_record[KEY_IDENTITY]
    if not identity in df_output.index:
        continue

    treatment_string = str(treatment_record[KEY_TREATMENT_STRING]).lower()
    for keyword in REQUIRED_TREATMENT_KEYWORDS:
        if keyword in treatment_string:
            # print(f'Treatment keyword matched: #{identity} {keyword}')
            column_name = map_column_name(keyword)
            df_output.loc[identity, column_name] = True

if DROP_NA != False:
    df_output.dropna(inplace=True)


# collect exam items

print('Collecting exam items...')

if TEST_MODE:
    df_exam = pd.read_csv(
        FILTERED_EXAM_PATH,
        usecols=[KEY_IDENTITY, KEY_EXAM_NAME, KEY_EXAM_RESULT],
        nrows=TEST_ROWS,  # for quick test
    )
else:
    df_exam = pd.read_csv(
        FILTERED_EXAM_PATH,
        usecols=[KEY_IDENTITY, KEY_EXAM_NAME, KEY_EXAM_RESULT],
    )

exam_record_count = len(df_exam)
exam_item_dict = dict(
    [item_name, dict([identity, np.nan] for identity in df_output.index)]
    for item_name in REQUIRED_EXAM_ITEMS
)
for exam_index in df_exam.index:
    print(f'\tProcessing exam record {exam_index + 1:7}/{exam_record_count}')
    exam_record = df_exam.iloc[exam_index]
    item_name = exam_record[KEY_EXAM_NAME]
    if item_name in exam_item_dict:
        item_record = exam_item_dict[item_name]
        identity = exam_record[KEY_IDENTITY]
        if identity in item_record:
            item_record[identity] = exam_record[KEY_EXAM_RESULT]

for item_name, item_record in exam_item_dict.items():
    exam_item_record = exam_item_dict[item_name]
    column_name = map_column_name(item_name)
    df_output[column_name] = df_output.index.map(
        exam_item_record.__getitem__
    )

if DROP_NA == 'all':
    df_output.dropna(inplace=True)


# collect lab variables

print('Collecting lab variables...')

if TEST_MODE:
    df_lab = pd.read_csv(
        FILTERED_LAB_PATH,
        usecols=[KEY_IDENTITY, KEY_LAB_NAME, KEY_LAB_RESULT],
        nrows=TEST_ROWS,
    )
else:
    df_lab = pd.read_csv(
        FILTERED_LAB_PATH,
        usecols=[KEY_IDENTITY, KEY_LAB_NAME, KEY_LAB_RESULT],
    )

lab_record_count = len(df_lab)
lab_var_dict = dict(
    [var_name, dict()]
    for var_name in REQUIRED_LAB_VARIABLES
)
for lab_index in df_lab.index:
    print(f'\tProcessing lab record {lab_index + 1:7}/{lab_record_count}')
    lab_record = df_lab.iloc[lab_index]
    var_name = lab_record[KEY_LAB_NAME]
    if var_name in lab_var_dict:
        var_record = lab_var_dict[var_name]
        identity = lab_record[KEY_IDENTITY]
        if identity in var_record:
            var_record[identity].append(
                lab_record[KEY_LAB_RESULT]
            )
        else:
            var_record[identity] = [lab_record[KEY_LAB_RESULT]]

for var_name, var_record in lab_var_dict.items():
    lab_var_record = lab_var_dict[var_name]
    column_name = map_column_name(var_name)
    df_output[column_name] = df_output.index.map(
        lambda identity: (
            mean(lab_var_record[identity])
            if identity in lab_var_record else np.nan
        )
    )

if DROP_NA == 'all':
    df_output.dropna(inplace=True)


# additional modification
print('Post-processing...')
if COMPACT_MODE:
    post_process_compact(df_output)
else:
    post_process_full(df_output)


# output to file
print('Writing to file...')
if DROP_NA == 'all':
    df_output.dropna(inplace=True)
if COMPRESS_OUTPUT:
    df_output.to_csv(
        OUTPUT_PATH,
        compression='gzip',
    )
else:
    df_output.to_csv(
        OUTPUT_PATH,
    )


# success message
print('Done.')
