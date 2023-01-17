from sklearn.model_selection import StratifiedGroupKFold

SEED = 1011
SCORING = ['accuracy', 'roc_auc']

CV_FOLDS = 10
cv = StratifiedGroupKFold(
    n_splits=CV_FOLDS,
    shuffle=True,
    random_state=SEED,
)
