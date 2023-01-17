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
INFUSION_PATH = eicu_path('infusionDrug.csv.gz')
APACHE_PATH = eicu_path('apachePatientResult.csv.gz')

SEPSIS_KEYWORD = 'sepsis'
KEY_IDENTITY = 'patientunitstayid'
KEY_OFFSET = 'offset'
KEY_DIAGNOSIS_STRING = 'diagnosisstring'
KEY_TREATMENT_OFFSET = 'treatmentoffset'
KEY_TREATMENT_STRING = 'treatmentstring'
KEY_EXAM_OFFSET = 'physicalexamoffset'
KEY_EXAM_NAME = 'physicalexampath'
KEY_EXAM_RESULT = 'physicalexamtext'
KEY_LAB_OFFSET = 'labresultoffset'
KEY_LAB_NAME = 'labname'
KEY_LAB_RESULT = 'labresult'
KEY_PERIODIC_OFFSET = 'observationoffset'
KEY_APERIODIC_OFFSET = 'observationoffset'
KEY_INFUSION_OFFSET = 'infusionoffset'
KEY_INFUSION_NAME = 'drugname'
KEY_INFUSION_AMOUNT = 'drugamount'
KEY_APACHE_SCORE = 'apachescore'
KEY_APACHE_VERSION = 'apacheversion'

# -- variables to find --
# APACHE-IV (ICU admission)
# Plateau pressure (Daily, if ventilated)
# Tidal volume (Daily, if ventilated)
# RSBI (Daily, if ventilated; RSBI = respiration_rate / tidal_volume)
# Respiratory SOFA (Daily)
# Liver SOFA (Daily)
# Renal SOFA (Daily)
# Cardiovascular SOFA (Daily)
# Heparin days (Before assessment)
# MV durations (Before assessment)

EXPECTED_APACHE_VERSION = 'IV'

NON_TEMPORAL_COLUMNS_COMPACT = [
    # TODO:
]
NON_TEMPORAL_COLUMNS_FULL = [
    *NON_TEMPORAL_COLUMNS_COMPACT,
    'age',
    'gender',
    'ethnicity',
    'admissionheight',  # height
]

LAB_VARIABLES_COMPACT = [
    # TODO:
]
LAB_VARIABLES_FULL = [
    *LAB_VARIABLES_COMPACT,
    'creatinine',  # Creatinine (mg/dL)
    'platelets x 1000',  # Platelet (K/mcL)
    'PT - INR',  # INR (international normalized ratio; ratio)
    'PT',  # PT (prothrombin time; sec)
    'PTT',  # PTT (???; sec)
    'lactate',  # Lactate (mmol/L)
    'RDW',  # RDW (red cell volume distribution width)
    'total bilirubin',  # Total bilirubin (mg/dL)
    'direct bilirubin',  # Direct bilirubin (mg/dL)
    'bicarbonate',  # Bicarbonate (mmol/L)
    'CRP',  # C-Reactive Protein (mg/dL)
    '-lymphs',  # lymphocytes (%; normal: 20%~40%)
    'albumin',  # Albumin (g/dL)
    'prealbumin',  # pre-albumin (mg/dL)
    'WBC x 1000',  # WBC (white blood cell; 1000 K/mcL)
    'total protein',  # Total protein (g/dL)
    'anion gap',  # Anion gap (mmol/L?)
    'BUN',  # BUN (mg/dL)
    'fibrinogen',  # Fibrinogen (mg/dL)
    'MCH',  # MCH (pg)
    'MCHC',  # MCHC (g/dL)
    'MCV',  # MCV (fL)
    'ALT (SGPT)',  # ALT (SGPT) (Units/L)
    'AST (SGOT)',  # AST (SGOT) (Units/L)
    'RBC',  # RBC (M/mcL)
    'pH',  # pH value
    'paO2',  # paO2 (mm Hg)
    'paCO2',  # paCO2 (mm Hg)
    'FiO2',  # FiO2 (%)
    'Total CO2',  # Total CO2
    'chloride',  # chloride (mmol/L)
    'calcium',  # calcium (mg/dL)
    'potassium',  # potassium (mmol/L)
    'sodium',  # sodium (mmol/L)
    'glucose',  # glucose (mg/dL)
    'Base Excess',  # BE (Base Excess; mEq/L)
    'Hct',  # Hematocrit HCT (%)
    'Methemoglobin',  # Hemoglobin? (%)
]

# path -> alias
EXAM_ITEM_MAP_COMPACT = {
    # TODO:
}
EXAM_ITEM_MAP_FULL = {
    **EXAM_ITEM_MAP_COMPACT,
    # Weight (kg)
    'notes/Progress Notes/Physical Exam/Physical Exam'
    '/Constitutional/Weight and I&O/Weight (kg)/Current': 'weight',
    # Urine output (mL)
    'notes/Progress Notes/Physical Exam/Physical Exam'
    '/Constitutional/Weight and I&O/I&&O (ml)/Urine': 'urine',
    # TODO: extract score from path
    # GCS (Daily)
    # 'notes/Progress Notes/Physical Exam/Physical Exam'
    # '/Neurologic/GCS/{score}': 'GCS',
    # PEEP (Daily, if ventilated)
    'notes/Progress Notes/Physical Exam/Physical Exam'
    '/Constitutional/Vital Sign and Physiological Data/PEEP/PEEP': 'PEEP',
}

EXAM_ITEMS_COMPACT = list(EXAM_ITEM_MAP_COMPACT.keys())
EXAM_ITEMS_FULL = list(EXAM_ITEM_MAP_FULL.keys())

# in lower case
TREATMENT_KEYWORDS_COMPACT = [
    # TODO:
]
TREATMENT_KEYWORDS_FULL = [
    *TREATMENT_KEYWORDS_COMPACT,
    'vasopressor',  # Vasopressor use
    'heparin',  # Heparin use
]

APERIODIC_COLUMNS_COMPACT = [
    # TODO:
]
APERIODIC_COLUMNS_FULL = [
    *APERIODIC_COLUMNS_COMPACT,
    'noninvasivemean',  # Non-invasive mean blood pressure (mmHg?)
]

PERIODIC_COLUMNS_COMPACT = [
    # TODO:
]
PERIODIC_COLUMNS_FULL = [
    *PERIODIC_COLUMNS_COMPACT,
    'heartrate',  # Heart rate (per minute?)
    'respiration',  # Respiratory rate (per minute?)
    'sao2',  # SpO2 (https://eicu-crd.mit.edu/eicutables/vitalperiodic/)
    'temperature',  # Temperature (in celsius)
]

# in lower case
INFUSION_KEYWORDS_COMPACT = [
    # TODO:
]
INFUSION_KEYWORDS_FULL = [
    *INFUSION_KEYWORDS_COMPACT,
    'rbc',  # RBC Transfusion (Sum of 24 hours; ml/hr)
    'ffp',  # FFP Transfusion (Sum of 24 hours; ml/hr)
    'plt',  # PLT Transfusion (Sum of 24 hours; ml/hr)
]

# rename map (source -> alias)
COLUMN_ALIASES = {
    **EXAM_ITEM_MAP_FULL,
    'admissionheight': 'height',
    'platelets x 1000': 'platelet',
    'PT - INR': 'INR',
    '-lymphs': 'lymph',
    'WBC x 1000': 'WBC',
    'noninvasivemean': 'MAP',
    'heartrate': 'heart rate',
    'respiration': 'respiration rate',
    'sao2': 'SpO2',
    'rbc': 'RBC transfusion',
    'ffp': 'FFP transfusion',
    'plt': 'PLT transfusion',
    'ALT (SGPT)': 'ALT',
    'AST (SGOT)': 'AST',
    'apachescore': 'Apache-IV',
}

CATEGORICAL_COLUMNS_COMPACT = [
    # TODO:
]
CATEGORICAL_COLUMNS_FULL = [
    *CATEGORICAL_COLUMNS_COMPACT,
    'gender',
    'ethnicity',
    'vasopressor',
    'heparin',
]

CUMULATIVE_COLUMNS_COMPACT = [
    # TODO:
]
CUMULATIVE_COLUMNS_FULL = [
    *CUMULATIVE_COLUMNS_COMPACT,
    'urine',
    'RBC transfusion',
    'FFP transfusion',
    'PLT transfusion',
]

# column_name -> indicator
PICS_CONDITIONS = {
    'offset': lambda v: v >= 10,
    'CRP': lambda v: v > 3.2,
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
