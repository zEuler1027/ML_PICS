import numpy as np
from os import path
from math import floor
import sys

BASE_DIR = path.dirname(__file__)


def relative_path(p):
    '''
    Returns `path.join(BASE_DIR, p)`.
    '''
    return path.join(BASE_DIR, p)


EICU_DIR = relative_path('../physionet.org/files/eicu-crd/2.0/')


def eicu_path(p):
    '''
    Returns `path.join(EICU_DIR, p)`.
    '''
    return path.join(EICU_DIR, p)


CATALOGUE_PATH = relative_path('catalogue_eicu.json')
LAB_PATH = eicu_path('lab.csv.gz')
EXAM_PATH = eicu_path('physicalExam.csv.gz')
TREATMENT_PATH = eicu_path('treatment.csv.gz')

# configs

TEST_ROWS = 5000
MINUTES_PER_DAY = 24 * 60
KEY_IDENTITY = 'patientunitstayid'
KEY_OFFSET = 'offset'
KEY_TREATMENT_OFFSET = 'treatmentoffset'
KEY_TREATMENT_STRING = 'treatmentstring'
KEY_EXAM_OFFSET = 'physicalexamoffset'
KEY_EXAM_NAME = 'physicalexamvalue'
KEY_EXAM_RESULT = 'physicalexamtext'
KEY_LAB_OFFSET = 'labresultoffset'
KEY_LAB_NAME = 'labname'
KEY_LAB_RESULT = 'labresult'

TREATMENT_USE_COLS = [
    KEY_IDENTITY,
    KEY_TREATMENT_OFFSET,
    KEY_TREATMENT_STRING,
]
EXAM_USE_COLS = [
    KEY_IDENTITY,
    KEY_EXAM_OFFSET,
    KEY_EXAM_NAME,
    KEY_EXAM_RESULT,
]
LAB_USE_COLS = [
    KEY_IDENTITY,
    KEY_LAB_OFFSET,
    KEY_LAB_NAME,
    KEY_LAB_RESULT,
]

MIN_OFFSET = 1

REQUIRED_COLUMNS = [
    # -- compact model --
    'age',
    'meanbp',  # MAP(mean artery pressure)
    'wbc',  # WBC(white blood cell)
    'urine',  # Urine output
    # -- full model --
    # 'admissionweight',  # weight
    # 'admissionheight',  # height
    # TBC
]

REQUIRED_LAB_VARIABLES = [  # compact model
    'creatinine',  # Creatinine (mg/dL)
    'platelets x 1000',  # Platelet (K/mcL)
    'PT - INR',  # INR (international normalized ratio; ratio)
    'PT',  # PT (prothrombin time; sec)
    'PTT',  # PTT (???; sec)
    'lactate',  # Lactate (mmol/L)
    'RDW',  # RDW (red cell volume distribution width; )
    'total bilirubin',  # Total bilirubin (mg/dL)
    'bicarbonate',  # Bicarbonate (mmol/L)
    'CRP',  # C-Reactive Protein (mg/dL)
    '-lymphs',  # lymphocytes (%; normal: 20%~40%)
    'albumin',  # Albumin (g/dL)
    'prealbumin',  # pre-albumin (mg/dL)
]

REQUIRED_EXAM_ITEMS = [
    'HR Current',  # Heart rate
]

REQUIRED_TREATMENT_KEYWORDS = [  # in lower case
    'vasopressor',  # Vasopressor use
]

# rename map (source->alias)
COLUMN_ALIASES = {
    'admissionweight': 'weight',
    'admissionheight': 'height',
    'platelets x 1000': 'platelet',
    'PT - INR': 'inr',
    'PT': 'pt',
    'PTT': 'ptt',
    'RDW': 'rdw',
    'total bilirubin': 'bilirubin',
    'HR Current': 'hr',
    'CRP': 'crp',
    '-lymphs': 'lymph',
}

# column_name -> indicator
PICS_CONDITIONS = {
    'offset': lambda v: v >= 10,
    'crp': lambda v: v > 3.2,
    'lymph': lambda v: v < 20,
    'albumin': lambda v: v < 3,
    'prealbumin': lambda v: v < 10,
}


def offset2days(offset):
    return floor(offset / MINUTES_PER_DAY)


def map_column_name(column_name):
    '''
    Returns corresponding column alias
    if `column_name` is in `COLUMN_ALIASES`;
    otherwise, returns `column_name` as is.
    '''
    if column_name in COLUMN_ALIASES:
        return COLUMN_ALIASES[column_name]
    else:
        return column_name


def mean(values):
    count = len(values)
    if count == 0:
        return np.nan
    else:
        return sum(values) / count


class SimpleProgress:

    def __init__(self, values):
        self.values = values
        self.n = len(values)
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        n = self.n
        i = self.i
        if i == n:
            sys.stdout.write('\n')
            raise StopIteration()
        else:
            pct = (i + 1) / n
            if i:
                sys.stdout.write('\r')
            sys.stdout.write(f'{pct:.2%}')
            sys.stdout.flush()
            self.i += 1
            return self.values[i]
