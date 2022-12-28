#!/usr/bin/python3
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('exam_filtered_test.csv')
    df_exam = pd.read_csv(
        EXAM_PATH,
        usecols=[KEY_IDENTITY, KEY_EXAM_NAME, KEY_EXAM_RESULT],
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('exam_filtered.csv.gz')
    df_exam = pd.read_csv(
        EXAM_PATH,
        usecols=[KEY_IDENTITY, KEY_EXAM_NAME, KEY_EXAM_RESULT],
    )

values = {
    KEY_EXAM_NAME: REQUIRED_EXAM_ITEMS,
}
filter_mask = df_exam.isin(values).any(1)
df_filtered = df_exam[filter_mask]

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
