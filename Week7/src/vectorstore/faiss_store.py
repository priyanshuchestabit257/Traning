import faiss
import pickle
import numpy as np
from pathlib import Path


VECTOR_DIR = Path("src/vectorstore")
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_DIR / "faiss.index"
META_PATH = VECTOR_DIR / "metadata.pkl"


class FaissStore:
    def __init__(self, dim):
        self.dim = dim

        if INDEX_PATH.exists():
            self.index = faiss.read_index(str(INDEX_PATH))
            with open(META_PATH, "rb") as f:
                self.texts = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.texts = []

    def add(self, vectors: np.ndarray, texts: list):
        self.index.add(vectors)
        self.texts.extend(texts)
        self.save()

    def save(self):
        faiss.write_index(self.index, str(INDEX_PATH))
        with open(META_PATH, "wb") as f:
            pickle.dump(self.texts, f)

    def search(self, query_vector: np.ndarray, k: int = 5):
        distances, indices = self.index.search(query_vector, k)
        results = [self.texts[i] for i in indices[0]]
        return results
