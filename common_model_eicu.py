import pandas as pd
import numpy as np
from common_eicu import CATEGORICAL_COLUMNS
from sklearn.model_selection import StratifiedGroupKFold

SEED = 1011
SCORING = ['accuracy', 'roc_auc']

CV_FOLDS = 10
cv = StratifiedGroupKFold(
    n_splits=CV_FOLDS,
    shuffle=True,
    random_state=SEED,
)


def get_full_data():

    df_data = pd.read_csv('./data/data_eicu_full.csv.gz')

    # clamp infinite values
    df_data.replace(np.inf, 9999, inplace=True)

    # set categorical columns
    for column_name in CATEGORICAL_COLUMNS:
        df_data[column_name] = df_data[column_name].astype('category')

    return df_data
