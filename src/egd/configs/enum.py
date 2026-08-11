# /egd/configs/enum.py

from enum import Enum


class CNNSize(Enum):
    B0 = "b0"
    B1 = "b1"
    B2 = "b2"
    B3 = "b3"
    B4 = "b4"
    B5 = "b5"
    B6 = "b6"
    B7 = "b7"


class VITSize(Enum):
    XXS = "xxs"
    XS = "xs"
    S = "s"


class AnatomyClass(Enum):
    ESOPHAGUS = "esophagus"
    SQUAMOCOLUMNAR_JUNCTION = "squamocolumnar_junction"
    FUNDUS = "fundus"
    BODY_ANTEGRADE = "body_antegrade"
    BODY_RETROFLEX = "body_retroflex"
    ANGULUS = "angulus"
    ANTRUM = "antrum"
    DUODENAL_BULB = "duodenal_bulb"
    DESCENDING_PART_OF_DUODENUM = "descending_part_of_duodenum"


class DiseaseClass(Enum):
    NORMAL = "normal"
    ESOPHAGEAL_NEOPLASM = "esophageal_neoplasm"
    ESOPHAGEAL_VARICES = "esophageal_varices"
    GASTROESOPHAGEAL_REFLUX_DISEASE = "gastroesophageal_reflux_disease"
    GASTRIC_NEOPLASM = "gastric_neoplasm"
    GASTRIC_POLYP = "gastric_polyp"
    GASTRIC_ULCER = "gastric_ulcer"
    GASTRIC_VARICES = "gastric_varices"
    DUODENAL_DISEASES_BULB = "duodenal_diseases(bulb)"
    DUODENAL_DISEASES_DESCENDING = "duodenal_diseases(descending)"
