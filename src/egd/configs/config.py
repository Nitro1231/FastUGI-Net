# /egd/configs/config.py

import torch
from dataclasses import dataclass, field
from egd.configs.enum import CNNSize, VITSize, AnatomyClass, DiseaseClass
from egd.configs.constant import ANATOMICAL_CLASSES, DISEASE_CLASSES, MEAN, STD

@dataclass
class ModelConfig:
    model_name: str
    weights_path: str
    cnn_size: CNNSize
    vit_size: VITSize
    anatomical_classes: list[AnatomyClass] = field(default_factory=lambda: list(ANATOMICAL_CLASSES))
    disease_classes: list[DiseaseClass] = field(default_factory=lambda: list(DISEASE_CLASSES))
    normalize_mean: list[float] = field(default_factory=lambda: list(MEAN))
    normalize_std: list[float] = field(default_factory=lambda: list(STD))
    device: str | torch.device = "auto"

    def __post_init__(self):
        if self.device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(self.device)
