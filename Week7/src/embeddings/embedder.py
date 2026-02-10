from sentence_transformers import SentenceTransformer
import numpy as np

class BGEEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-base-en")

    def embed(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        return embeddings