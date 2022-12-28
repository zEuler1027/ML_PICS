#!/usr/bin/python3
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('lab_filtered_test.csv')
    df_lab = pd.read_csv(
        LAB_PATH,
        usecols=[KEY_IDENTITY, KEY_LAB_NAME, KEY_LAB_RESULT],
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('lab_filtered.csv.gz')
    df_lab = pd.read_csv(
        LAB_PATH,
        usecols=[KEY_IDENTITY, KEY_LAB_NAME, KEY_LAB_RESULT],
    )

values = {
    KEY_LAB_NAME: REQUIRED_LAB_VARIABLES,
}
filter_mask = df_lab.isin(values).any(1)
df_filtered = df_lab[filter_mask]

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
