#!/usr/bin/env python3
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('exam_eicu_filtered_test.csv')
    df_exam = pd.read_csv(
        EXAM_PATH,
        usecols=EXAM_USE_COLS,
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('exam_eicu_filtered.csv.gz')
    df_exam = pd.read_csv(
        EXAM_PATH,
        usecols=EXAM_USE_COLS,
    )

# filter exam items
values = {
    KEY_EXAM_NAME: EXAM_ITEMS_FULL,
}
filter_mask = df_exam.isin(values).any(axis='columns')
df_filtered = df_exam[filter_mask].copy()

# transform offset
df_filtered[KEY_EXAM_OFFSET] = \
    df_filtered[KEY_EXAM_OFFSET].map(offset2days)

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
