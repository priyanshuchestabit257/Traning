import faiss
import json
from pathlib import Path
from rank_bm25 import BM25Okapi

from src.embeddings.embedder import BGEEmbedder
from src.retriever.reranker import CosineReranker


class HybridRetriever:
    def __init__(self):
        self.embedder = BGEEmbedder()
        self.reranker = CosineReranker()

        # Load FAISS
        self.index = faiss.read_index("src/vectorstore/index.faiss")

        # Load stored chunks
        self.chunks = []
        for f in Path("src/data/chunks").glob("*.jsonl"):
            with open(f, "r", encoding="utf-8") as file:
                for line in file:
                    self.chunks.append(json.loads(line))

        # BM25 setup
        corpus = [c["text"].split() for c in self.chunks]
        self.bm25 = BM25Okapi(corpus)

    def _filter_chunks(self, filters: dict):
        if not filters:
            return self.chunks

        filtered = []
        for c in self.chunks:
            meta = c.get("metadata", {})
            if all(meta.get(k) == v for k, v in filters.items()):
                filtered.append(c)
        return filtered

    def search(self, query: str, top_k: int = 5, filters: dict | None = None):
        # Apply metadata filters
        candidates = self._filter_chunks(filters)

        # ---------- Semantic Search ----------
        query_emb = self.embedder.embed([query])
        _, idxs = self.index.search(query_emb, top_k * 2)
        semantic_hits = [candidates[i] for i in idxs[0] if i < len(candidates)]

        # ---------- Keyword Search (BM25 fallback) ----------
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_hits = sorted(
            zip(candidates, bm25_scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        bm25_hits = [c[0] for c in bm25_hits]

        # ---------- Merge + Deduplicate ----------
        merged = {c["text"]: c for c in semantic_hits + bm25_hits}
        merged_chunks = list(merged.values())

        
        final_chunks = self.reranker.rerank(query, merged_chunks, top_k)

        return final_chunks
