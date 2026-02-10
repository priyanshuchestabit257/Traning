from src.retriever.hybrid_retriever import HybridRetriever


class ContextBuilder:
    def __init__(self):
        self.retriever = HybridRetriever()

    def build_context(self, query: str, top_k: int = 5, filters: dict | None = None):
        chunks = self.retriever.search(query, top_k, filters)

        context_blocks = []
        sources = []

        for i, c in enumerate(chunks):
            context_blocks.append(
                f"[{i+1}] {c['text']}"
            )
            sources.append({
                "chunk_id": c["chunk_id"],
                "source": c["metadata"].get("source"),
                "page": c["metadata"].get("page"),
            })

        return {
            "context": "\n\n".join(context_blocks),
            "sources": sources
        }
