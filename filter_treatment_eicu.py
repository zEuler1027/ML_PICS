#!/usr/bin/env python
import pandas as pd
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

if TEST_MODE:
    OUTPUT_PATH = relative_path('treatment_eicu_filtered_test.csv')
    df_treatment = pd.read_csv(
        TREATMENT_PATH,
        usecols=TREATMENT_USE_COLS,
        nrows=TEST_ROWS,
    )
else:
    OUTPUT_PATH = relative_path('treatment_eicu_filtered.csv.gz')
    df_treatment = pd.read_csv(
        TREATMENT_PATH,
        usecols=TREATMENT_USE_COLS,
    )

# filter treatment strings
filter_mask = df_treatment[KEY_TREATMENT_STRING].map(
    lambda treatment_string: any(
        keyword in treatment_string
        for keyword in TREATMENT_KEYWORDS_FULL
    )
)
df_filtered = df_treatment[filter_mask].copy()

# transform offset
df_filtered[KEY_TREATMENT_OFFSET] = \
    df_filtered[KEY_TREATMENT_OFFSET].map(offset2days)

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
