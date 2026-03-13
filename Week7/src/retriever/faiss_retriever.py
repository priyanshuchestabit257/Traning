import json
from pathlib import Path
import numpy as np
import faiss

from src.embeddings.embedder import BGEEmbedder
from src.vectorstore.faiss_store import FaissStore


CHUNKS_DIR = Path("src/data/chunks")

embedder = BGEEmbedder()

# Initialize FAISS store (auto loads index)
store = FaissStore(dim=768)


# Load all chunks (optional depending on your pipeline)
all_chunks = []
for file in CHUNKS_DIR.glob("*.jsonl"):
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            all_chunks.append(json.loads(line))


def retrieve(query, k=3):

    query_embedding = embedder.embed_query(query)

    # Normalize for cosine similarity
    faiss.normalize_L2(query_embedding)

    distances, indices = store.index.search(query_embedding, k)

    if indices is None or len(indices[0]) == 0:
        return "", 0.0

    retrieved_docs = []
    for idx in indices[0]:
        if idx != -1:
            retrieved_docs.append(store.texts[idx])

    if not retrieved_docs:
        return "", 0.0

    context = "\n\n".join(retrieved_docs)
    similarity = float(distances[0][0])

    print("\n--- RETRIEVED CONTEXT ---")
    print(context)
    print("--- SIMILARITY ---", similarity)

    return context, similarity