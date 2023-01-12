import numpy as np
from os import path
from common import *

EICU_DIR = relative_path('../physionet.org/files/eicu-crd/2.0/')


def eicu_path(p):
    '''
    Returns `path.join(EICU_DIR, p)`.
    '''
    return path.join(EICU_DIR, p)


CATALOGUE_PATH = relative_path('./data/catalogue_eicu_single.json')
LAB_PATH = eicu_path('lab.csv.gz')
EXAM_PATH = eicu_path('physicalExam.csv.gz')
TREATMENT_PATH = eicu_path('treatment.csv.gz')
DIAGNOSIS_PATH = eicu_path('diagnosis.csv.gz')
PERIODIC_PATH = eicu_path('vitalPeriodic.csv.gz')
APERIODIC_PATH = eicu_path('vitalAperiodic.csv.gz')

SEPSIS_KEYWORD = 'sepsis'
KEY_IDENTITY = 'patientunitstayid'
KEY_OFFSET = 'offset'
KEY_DIAGNOSIS_STRING = 'diagnosisstring'
KEY_TREATMENT_OFFSET = 'treatmentoffset'
KEY_TREATMENT_STRING = 'treatmentstring'
KEY_EXAM_OFFSET = 'physicalexamoffset'
KEY_EXAM_NAME = 'physicalexamvalue'
KEY_EXAM_RESULT = 'physicalexamtext'
KEY_LAB_OFFSET = 'labresultoffset'
KEY_LAB_NAME = 'labname'
KEY_LAB_RESULT = 'labresult'
KEY_PERIODIC_OFFSET = 'observationoffset'
KEY_APERIODIC_OFFSET = 'observationoffset'

NON_TEMPORAL_COLUMNS_COMPACT = [
    'age',
]
NON_TEMPORAL_COLUMNS_FULL = [
    *NON_TEMPORAL_COLUMNS_COMPACT,
    'gender',
    'ethnicity',
    'admissionweight',  # weight
    'admissionheight',  # height
    # TODO:
]

LAB_VARIABLES_COMPACT = [
    'creatinine',  # Creatinine (mg/dL)
    'platelets x 1000',  # Platelet (K/mcL)
    'PT - INR',  # INR (international normalized ratio; ratio)
    'PT',  # PT (prothrombin time; sec)
    'PTT',  # PTT (???; sec)
    'lactate',  # Lactate (mmol/L)
    'RDW',  # RDW (red cell volume distribution width)
    'total bilirubin',  # Total bilirubin (mg/dL)
    'bicarbonate',  # Bicarbonate (mmol/L)
    'CRP',  # C-Reactive Protein (mg/dL)
    '-lymphs',  # lymphocytes (%; normal: 20%~40%)
    'albumin',  # Albumin (g/dL)
    'prealbumin',  # pre-albumin (mg/dL)
    'WBC x 1000',  # WBC (white blood cell; 1000 K/mcL)
]
LAB_VARIABLES_FULL = [
    *LAB_VARIABLES_COMPACT,
    # TODO:
]

EXAM_ITEMS_COMPACT = [
    'Urine',  # Urine output (mL?)
]
EXAM_ITEMS_FULL = [
    *EXAM_ITEMS_COMPACT,
    # TODO:
]

# in lower case
TREATMENT_KEYWORDS_COMPACT = [
    'vasopressor',  # Vasopressor use
]
TREATMENT_KEYWORDS_FULL = [
    *TREATMENT_KEYWORDS_COMPACT,
    # TODO:
]

APERIODIC_COLUMNS_COMPACT = [
    'noninvasivemean',  # Non-invasive mean blood pressure (mmHg?)
]
APERIODIC_COLUMNS_FULL = [
    *APERIODIC_COLUMNS_COMPACT,
    # TODO:
]

PERIODIC_COLUMNS_COMPACT = [
    'heartrate',  # Heart rate (beats per minute?)
]
PERIODIC_COLUMNS_FULL = [
    *PERIODIC_COLUMNS_COMPACT,
    # TODO:
]

# rename map (source -> alias)
COLUMN_ALIASES = {
    'admissionweight': 'weight',
    'admissionheight': 'height',
    'platelets x 1000': 'platelet',
    'PT - INR': 'inr',
    'PT': 'pt',
    'PTT': 'ptt',
    'RDW': 'rdw',
    'total bilirubin': 'bilirubin',
    'heartrate': 'hr',
    'CRP': 'crp',
    '-lymphs': 'lymph',
    'Urine': 'urine',
    'WBC x 1000': 'wbc',
    'noninvasivemean': 'bp',
}

CATEGORICAL_COLUMNS_COMPACT = [
    'vasopressor',
]

CATEGORICAL_COLUMNS_FULL = [
    *CATEGORICAL_COLUMNS_COMPACT,
    # TODO:
]

# column_name -> indicator
PICS_CONDITIONS = {
    'offset': lambda v: v >= 10,
    'crp': lambda v: v > 3.2,
    'lymph': lambda v: v < 20,
    'albumin': lambda v: v < 3,
    'prealbumin': lambda v: v < 10,
}

CONDITION_ONLY_COLUMNS_FULL = [
    # None
]

CONDITION_ONLY_COLUMNS_COMPACT = [
    *CONDITION_ONLY_COLUMNS_FULL,
    # TODO:
]


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
