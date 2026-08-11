# /egd/model.py

import torch
import torchvision.transforms as T
import logging
from PIL import Image
from pathlib import Path
from egd.image import EGDImage
from egd.fastugi_net import FastUGINet
from egd.configs.config import ModelConfig
from egd.configs.constant import PREFIX_MAP


logger = logging.getLogger(__name__)

class Model:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = FastUGINet(
            anatomical_classes=len(config.anatomical_classes),
            disease_classes=len(config.disease_classes),
            cnn_size=config.cnn_size,
            vit_size=config.vit_size
        )
        state_dict = torch.load(config.weights_path, map_location=config.device, weights_only=False)
        self.model.load_state_dict(self._remap_state_dict(state_dict), strict=True)
        self.model.to(config.device)
        self.model.eval()
        logger.info(f"Model {config.model_name} loaded from {config.weights_path}.")

    def _remap_state_dict(self, state_dict):
        remapped = {}
        for key, value in state_dict.items():
            new_key = key
            for src, dst in PREFIX_MAP.items():
                if key.startswith(src):
                    new_key = dst + key[len(src):]
                    break
            remapped[new_key] = value
        return remapped

    def preprocess(self, image: Image.Image) -> torch.Tensor:
        x = T.Compose([
            T.ToTensor(),
            T.ConvertImageDtype(torch.float32),
        ])(image.convert("RGB"))
        _, h, w = x.shape
        x = T.CenterCrop(min(h, w))(x)
        x = T.Resize([224, 224], interpolation=T.InterpolationMode.BICUBIC, antialias=True)(x)
        x = T.Normalize(self.config.normalize_mean, self.config.normalize_std)(x)
        return x.unsqueeze(0)

    @torch.no_grad()
    def predict(self, image_path: Path) -> EGDImage:
        image = Image.open(image_path).convert("RGB")
        preprocessed_image = self.preprocess(image).to(self.config.device)

        anat_logits, disease_logits = self.model(preprocessed_image)
        anat_probs = torch.softmax(anat_logits, dim=1)[0]
        disease_probs = torch.softmax(disease_logits, dim=1)[0]
        anat_idx = anat_probs.argmax().item()
        disease_idx = disease_probs.argmax().item()

        return EGDImage(
            image_path=Path(image_path),
            original_image=image,
            preprocssed_image=preprocessed_image,
            anatomical_classes=self.config.anatomical_classes,
            disease_classes=self.config.disease_classes,
            anatomical_probabilities=anat_probs.tolist(),
            disease_probabilities=disease_probs.tolist(),
            anatomical_index=anat_idx,
            disease_index=disease_idx,
            mean=self.config.normalize_mean,
            std=self.config.normalize_std,            
        )
