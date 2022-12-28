#!/usr/bin/python3
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('treatment_filtered_test.csv')
    df_treatment = pd.read_csv(
        TREATMENT_PATH,
        usecols=[KEY_IDENTITY, KEY_TREATMENT_STRING],
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('treatment_filtered.csv.gz')
    df_treatment = pd.read_csv(
        TREATMENT_PATH,
        usecols=[KEY_IDENTITY, KEY_TREATMENT_STRING],
    )

filter_mask = df_treatment[KEY_TREATMENT_STRING].map(
    lambda treatment_string: any(
        keyword in treatment_string
        for keyword in REQUIRED_TREATMENT_KEYWORDS
    )
)
df_filtered = df_treatment[filter_mask]

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
