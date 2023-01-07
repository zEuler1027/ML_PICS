#!/usr/bin/env python
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('sepsis_eicu_test.csv')
    df_diagnosis = pd.read_csv(
        DIAGNOSIS_PATH,
        usecols=DIAGNOSIS_USE_COLS,
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('sepsis_eicu.csv.gz')
    df_diagnosis = pd.read_csv(
        DIAGNOSIS_PATH,
        usecols=DIAGNOSIS_USE_COLS,
    )

# filter diagnosis strings
filter_mask = df_diagnosis[KEY_DIAGNOSIS_STRING].map(
    lambda diagnosis_string: (
        SEPSIS_KEYWORD in str(diagnosis_string).lower()
    )
)
df_filtered = df_diagnosis[filter_mask].copy()

if TEST_MODE:
    df_filtered.to_csv(
        OUTPUT_PATH,
        index=False,
    )
else:
    df_filtered.to_csv(
        OUTPUT_PATH,
        compression='gzip',
        index=False,
    )

print('Done.')
