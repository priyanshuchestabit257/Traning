import faiss
import numpy as np
import pickle
from pathlib import Path

VECTOR_DIR = Path("src/vectorstore")
VECTOR_DIR.mkdir(exist_ok=True)

class FaissStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)

    def add(self, embeddings):
        self.index.add(embeddings)

    def save(self):
        faiss.write_index(self.index, str(VECTOR_DIR / "index.faiss"))

    def load(self):
        self.index = faiss.read_index(str(VECTOR_DIR / "index.faiss"))