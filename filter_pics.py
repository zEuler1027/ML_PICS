#!/usr/bin/python3
import pandas as pd
from functools import reduce
from common_eicu import *

TEST_MODE = False
# TEST_MODE = True

WITH_NA = True
# WITH_NA = False

if WITH_NA:
    DATA_PATH = relative_path('data_eicu_compact_sepsis_na.csv')
else:
    DATA_PATH = relative_path('data_eicu_compact_sepsis.csv')

if TEST_MODE:
    OUTPUT_PATH = relative_path('data_eicu_compact_pics_test.csv')
else:
    OUTPUT_PATH = relative_path('data_eicu_compact_pics.csv')

df_data = pd.read_csv(
    DATA_PATH,
    index_col=KEY_IDENTITY,
)

# drop rows that have any NA value in non-PICS-condition columns
column_set = set(df_data.columns)
condition_column_set = set(PICS_CONDITIONS.keys())
non_condition_columns = list(column_set - condition_column_set)
df_data.dropna(subset=non_condition_columns, inplace=True)

# remove entries with -1 (considered as NA)
mask_neg1 = (df_data == -1.0).any(axis='columns')
df_data = df_data[~mask_neg1]

df_data['pics'] = False  # init
df_data['decided'] = False  # init

for i in df_data.index:

    def map_mask(item):
        col, indicator = item
        value = df_data.at[i, col]
        if value != value:
            return value  # nan
        else:
            return indicator(value)

    masks = list(map(map_mask, PICS_CONDITIONS.items()))

    if any(v == False for v in masks):
        df_data.at[i, 'pics'] = False
        df_data.at[i, 'decided'] = True
    elif all(v == True for v in masks):
        df_data.at[i, 'pics'] = True
        df_data.at[i, 'decided'] = True

for col in PICS_CONDITIONS.keys():
    del df_data[col]

df_data = df_data[df_data['decided']]
del df_data['decided']

if TEST_MODE:
    df_data.to_csv(
        OUTPUT_PATH,
    )
else:
    df_data.to_csv(
        OUTPUT_PATH,
        # compression='gzip',
    )

print('Done.')
