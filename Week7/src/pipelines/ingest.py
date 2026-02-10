from pathlib import Path
import json

from src.embeddings.embedder import BGEEmbedder
from src.utils.loader import load_document
from src.utils.chunker import chunk_docs
from src.vectorstore.faiss_store import FaissStore

DATA_DIR = Path("src/data/raw")
CHUNKS_DIR = Path("src/data/chunks")

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx"}
MAX_EMBED_CHUNKS = 500


def ingest():
    embedder = BGEEmbedder()
    all_chunks = []

    if not DATA_DIR.exists():
        raise RuntimeError("src/data/raw directory does not exist")

    # Recursive scan
    files = [
        f for f in DATA_DIR.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not files:
        raise RuntimeError("No valid documents found in src/data/raw")

    print(f"Found {len(files)} valid documents")

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    for file in files:
        print(f"Loading: {file}")

        try:
            docs = load_document(str(file))
        except Exception as e:
            print(f"Failed to load {file.name}: {e}")
            continue

        if not docs:
            print(f"No content loaded from {file.name}")
            continue

        chunks = chunk_docs(docs)
        all_chunks.extend(chunks)

        # Store chunks to disk
        chunk_file = CHUNKS_DIR / f"{file.stem}.jsonl"
        with open(chunk_file, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks):
                record = {
                    "chunk_id": i,
                    "text": chunk.page_content,
                    "metadata": chunk.metadata,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"   → {len(chunks)} chunks stored")

    if not all_chunks:
        raise RuntimeError("Documents loaded but chunking produced no output")

    # LIMIT EMBEDDING TO 500 CHUNKS
    limited_chunks = all_chunks[:MAX_EMBED_CHUNKS]

    texts = [chunk.page_content for chunk in limited_chunks]
    embeddings = embedder.embed(texts)

    # FAISS store
    store = FaissStore(dim=embeddings.shape[1])
    store.add(embeddings)
    store.save()

    print("\nINGESTION SUMMARY")
    print(f" Total chunks created : {len(all_chunks)}")
    print(f"Chunks embedded      : {len(texts)} (limit={MAX_EMBED_CHUNKS})")
    print(f"Chunks stored in     : {CHUNKS_DIR}")


if __name__ == "__main__":
    ingest()
