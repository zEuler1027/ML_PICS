#!/usr/bin/python3
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

WITH_NA = True
# WITH_NA = False

if WITH_NA:
    RAW_DATA_PATH = relative_path('data_eicu_compact_raw_na.csv.gz')
else:
    RAW_DATA_PATH = relative_path('data_eicu_compact_raw.csv.gz')

DIAGNOSIS_PATH = eicu_path('diagnosis.csv.gz')
KEY_DIAGNOSIS_STRING = 'diagnosisstring'
SEPSIS_KEYWORD = 'sepsis'

OUTPUT_PATH = relative_path(
    'data_eicu_compact_sepsis'
    + ('_na' if WITH_NA else '')
    + ('_test' if TEST_MODE else '')
    + '.csv'
)

df_data_raw = pd.read_csv(
    RAW_DATA_PATH,
    index_col=KEY_IDENTITY,
)

if TEST_MODE:
    df_diagnosis = pd.read_csv(
        DIAGNOSIS_PATH,
        usecols=[KEY_IDENTITY, KEY_DIAGNOSIS_STRING],
        nrows=501,  # for quick test
    )
else:
    df_diagnosis = pd.read_csv(
        DIAGNOSIS_PATH,
        usecols=[KEY_IDENTITY, KEY_DIAGNOSIS_STRING],
    )

sepsis_flags = dict([identity, False] for identity in df_data_raw.index)
for diagnosis_index in df_diagnosis.index:
    identity = df_diagnosis.at[diagnosis_index, KEY_IDENTITY]
    if not identity in sepsis_flags:
        continue
    diagnosis_string = df_diagnosis.at[diagnosis_index, KEY_DIAGNOSIS_STRING]
    if SEPSIS_KEYWORD in diagnosis_string.lower():
        sepsis_flags[identity] = True

df_data_sepsis = df_data_raw[
    df_data_raw.index.map(sepsis_flags.__getitem__)
]

if TEST_MODE:
    df_data_sepsis.to_csv(
        OUTPUT_PATH,
    )
else:
    df_data_sepsis.to_csv(
        OUTPUT_PATH,
        # compression='gzip',
    )

print('Done.')
