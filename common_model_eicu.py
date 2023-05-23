import pandas as pd
import numpy as np
from common_eicu import CATEGORICAL_COLUMNS, KEY_OFFSET
from sklearn.model_selection import cross_validate, \
    StratifiedGroupKFold

SEED = 1011
SCORING = ['accuracy', 'roc_auc']

CV_FOLDS = 10
cv = StratifiedGroupKFold(
    n_splits=CV_FOLDS,
    shuffle=True,
    random_state=SEED,
)

COMPACT_COLUMNS = [
    KEY_OFFSET,
    'albumin',
    'lymph',
    'heart rate',
    'respiration rate',
    'total protein',
    'Hct',
    'creatinine',
    'pH',
    'calcium',
    'WBC',
    'BMI',
    'AST',
    'platelet',
    'MAP',
]

CATEGORICAL_COLUMNS_COMPACT = list(
    filter(
        lambda col: col in COMPACT_COLUMNS,
        CATEGORICAL_COLUMNS,
    )
)


def get_full_data(inf_replacement=9999):

    df_data = pd.read_csv('./data/data_eicu_full.csv.gz')

    # clamp infinite values
    df_data.replace(np.inf, inf_replacement, inplace=True)

    # set categorical columns
    for column_name in CATEGORICAL_COLUMNS:
        df_data[column_name] = df_data[column_name].astype('category')

    return df_data


def test_model(
    model,
    X,
    y,
    groups,
    *,
    return_result=False,
    n_jobs=None,
):

    scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=SCORING,
        groups=groups,
    )

    scores_accuracy = scores['test_accuracy']
    accuracy_mean = scores_accuracy.mean()
    accuracy_std = scores_accuracy.std()
    scores_auc = scores['test_roc_auc']
    auc_mean = scores_auc.mean()
    auc_std = scores_auc.std()

    print(f'>>> CV Result')
    print(f'accuracy_mean: {accuracy_mean:.4f}')
    print(f'accuracy_std:  {accuracy_std:.4f}')
    print(f'auc_mean:      {auc_mean:.4f}')
    print(f'auc_std:       {auc_std:.4f}')

    if return_result:
        return {
            'accuracy_mean': accuracy_mean,
            'accuracy_std': accuracy_std,
            'auc_mean': auc_mean,
            'auc_std': auc_std,
        }
