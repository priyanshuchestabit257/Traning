# src/embeddings/clip_embedder.py

import torch
import open_clip
from PIL import Image
import numpy as np

class CLIPEmbedder:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            model_name="ViT-B-32",
            pretrained="openai"
        )
        self.model = self.model.to(self.device)
        self.model.eval()

        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")

    def embed_image(self, image_path: str) -> np.ndarray:
        image = self.preprocess(
            Image.open(image_path).convert("RGB")
        ).unsqueeze(0).to(self.device)

        with torch.no_grad():
            features = self.model.encode_image(image)
            features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0]

    def embed_text(self, text: str) -> np.ndarray:
        tokens = self.tokenizer([text]).to(self.device)

        with torch.no_grad():
            features = self.model.encode_text(tokens)
            features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0]
