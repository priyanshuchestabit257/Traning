import numpy as np
from src.embeddings.embedder import BGEEmbedder


class CosineReranker:
    def __init__(self):
        self.embedder = BGEEmbedder()

    def rerank(self, query: str, chunks: list, top_k: int = 5):
        """
        Rerank chunks using cosine similarity between
        query embedding and chunk embeddings
        """
        if not chunks:
            return []

        query_emb = self.embedder.embed([query])[0]
        chunk_texts = [c["text"] for c in chunks]
        chunk_embs = self.embedder.embed(chunk_texts)

        scores = np.dot(chunk_embs, query_emb)

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [item[0] for item in ranked[:top_k]]
