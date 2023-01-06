#!/usr/bin/python3
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('lab_filtered_test.csv')
    df_lab = pd.read_csv(
        LAB_PATH,
        usecols=LAB_USE_COLS,
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('lab_filtered.csv.gz')
    df_lab = pd.read_csv(
        LAB_PATH,
        usecols=LAB_USE_COLS,
    )

# filter lab items
values = {
    KEY_LAB_NAME: REQUIRED_LAB_VARIABLES,
}
filter_mask = df_lab.isin(values).any(axis='columns')
df_filtered = df_lab[filter_mask].copy()

# transform offset
df_filtered[KEY_LAB_OFFSET] = \
    df_filtered[KEY_LAB_OFFSET].map(offset2days)

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
