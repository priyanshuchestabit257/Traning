import json
from pathlib import Path
import numpy as np
import faiss

from src.embeddings.embedder import BGEEmbedder
from src.vectorstore.faiss_store import FaissStore

CHUNKS_DIR = Path("src/data/chunks")

embedder = BGEEmbedder()

store = FaissStore(dim=768)

all_chunks = []
for file in CHUNKS_DIR.glob("*.jsonl"):
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            all_chunks.append(json.loads(line))


def retrieve(query, k=3):

    query_embedding = embedder.model.encode(query)
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

    faiss.normalize_L2(query_embedding)

    distances, indices = store.index.search(query_embedding, k)

    if indices is None or len(indices[0]) == 0:
        return "", 0.0

    retrieved_docs = []

    for idx in indices[0]:
        if idx != -1:

            doc = store.texts[idx]

            if hasattr(doc, "page_content"):
                retrieved_docs.append(doc.page_content)
            else:
                retrieved_docs.append(str(doc))

    if not retrieved_docs:
        return "", 0.0

    context = "\n\n".join(retrieved_docs)

    similarity = float(distances[0][0])

    print("\n--- RETRIEVED CONTEXT ---")
    print(context)
    print("\n--- SIMILARITY ---", similarity)

    return context, similarity