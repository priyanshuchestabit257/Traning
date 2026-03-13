import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)

        self.texts = []

    def add_memory(self, text):

        embedding = self.model.encode([text])
        self.index.add(np.array(embedding))

        self.texts.append(text)

    def search(self, query, k=3):

    # if no memory exists
        if len(self.texts) == 0:
         return []

        embedding = self.model.encode([query])

        distances, indices = self.index.search(np.array(embedding), k)

        results = []

        for i in indices[0]:
           if 0 <= i < len(self.texts):
            results.append(self.texts[i])

        return results