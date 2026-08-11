# /egd/configs/constant.py

from egd.configs.enum import AnatomyClass, DiseaseClass


MEAN = [0.5187, 0.2813, 0.2154]
STD = [0.2786, 0.1975, 0.1759]


PREFIX_MAP = {
    "conv1.": "backbone.0.",
    "block1.": "backbone.1.",
    "block2.": "backbone.2.",
    "block3.": "backbone.3.",
    "block4.": "backbone.4.",
    "conv.": "backbone.5.",
    "stages3.": "backbone.7.",
    "stages4.": "backbone.8.",
    "final_conv.": "backbone.9.",
}


ANATOMICAL_CLASSES = [
    AnatomyClass.ESOPHAGUS,
    AnatomyClass.SQUAMOCOLUMNAR_JUNCTION,
    AnatomyClass.FUNDUS,
    AnatomyClass.BODY_ANTEGRADE,
    AnatomyClass.BODY_RETROFLEX,
    AnatomyClass.ANGULUS,
    AnatomyClass.ANTRUM,
    AnatomyClass.DUODENAL_BULB,
    AnatomyClass.DESCENDING_PART_OF_DUODENUM,
]


ANATOMICAL_CLASSES_LABELS_EN = {
    AnatomyClass.ESOPHAGUS: "Esophagus",
    AnatomyClass.SQUAMOCOLUMNAR_JUNCTION: "Squamocolumnar Junction (SCJ)",
    AnatomyClass.FUNDUS: "Gastric Fundus",
    AnatomyClass.BODY_ANTEGRADE: "Gastric Body, Antegrade",
    AnatomyClass.BODY_RETROFLEX: "Gastric Body, Retroflex",
    AnatomyClass.ANGULUS: "Gastric Angulus",
    AnatomyClass.ANTRUM: "Gastric Antrum",
    AnatomyClass.DUODENAL_BULB: "Duodenal Bulb",
    AnatomyClass.DESCENDING_PART_OF_DUODENUM: "Descending Part of the Duodenum",
}


ANATOMICAL_CLASSES_LABELS_KR = {
    AnatomyClass.ESOPHAGUS: "식도",
    AnatomyClass.SQUAMOCOLUMNAR_JUNCTION: "편평원주상피접합부",
    AnatomyClass.FUNDUS: "위저부",
    AnatomyClass.BODY_ANTEGRADE: "위체부, 정방향",
    AnatomyClass.BODY_RETROFLEX: "위체부, 반전",
    AnatomyClass.ANGULUS: "위각절흔(위각)",
    AnatomyClass.ANTRUM: "위전정부",
    AnatomyClass.DUODENAL_BULB: "십이지장 구부",
    AnatomyClass.DESCENDING_PART_OF_DUODENUM: "십이지장 하행부",
}


DISEASE_CLASSES = [
    DiseaseClass.NORMAL,
    DiseaseClass.ESOPHAGEAL_NEOPLASM,
    DiseaseClass.ESOPHAGEAL_VARICES,
    DiseaseClass.GASTROESOPHAGEAL_REFLUX_DISEASE,
    DiseaseClass.GASTRIC_NEOPLASM,
    DiseaseClass.GASTRIC_POLYP,
    DiseaseClass.GASTRIC_ULCER,
    DiseaseClass.GASTRIC_VARICES,
    DiseaseClass.DUODENAL_DISEASES_BULB,
    DiseaseClass.DUODENAL_DISEASES_DESCENDING,
]


DISEASE_CLASSES_LABELS_EN = {
    DiseaseClass.NORMAL: "Normal",
    DiseaseClass.ESOPHAGEAL_NEOPLASM: "Esophageal Neoplasm",
    DiseaseClass.ESOPHAGEAL_VARICES: "Esophageal Varices",
    DiseaseClass.GASTROESOPHAGEAL_REFLUX_DISEASE: "Gastroesophageal Reflux Disease (GERD)",
    DiseaseClass.GASTRIC_NEOPLASM: "Gastric Neoplasm",
    DiseaseClass.GASTRIC_POLYP: "Gastric Polyp",
    DiseaseClass.GASTRIC_ULCER: "Gastric Ulcer",
    DiseaseClass.GASTRIC_VARICES: "Gastric Varices",
    DiseaseClass.DUODENAL_DISEASES_BULB: "Duodenal Diseases, Bulb",
    DiseaseClass.DUODENAL_DISEASES_DESCENDING: "Duodenal Diseases, Descending",
}


DISEASE_CLASSES_LABELS_KR = {
    DiseaseClass.NORMAL: "정상",
    DiseaseClass.ESOPHAGEAL_NEOPLASM: "식도 종양",
    DiseaseClass.ESOPHAGEAL_VARICES: "식도정맥류",
    DiseaseClass.GASTROESOPHAGEAL_REFLUX_DISEASE: "위식도역류질환",
    DiseaseClass.GASTRIC_NEOPLASM: "위 종양",
    DiseaseClass.GASTRIC_POLYP: "위 용종",
    DiseaseClass.GASTRIC_ULCER: "위 궤양",
    DiseaseClass.GASTRIC_VARICES: "위 정맥류",
    DiseaseClass.DUODENAL_DISEASES_BULB: "십이지장 구부 질환",
    DiseaseClass.DUODENAL_DISEASES_DESCENDING: "십이지장 하행부 질환",
}
