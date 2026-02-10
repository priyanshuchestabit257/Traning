from src.pipelines.context_builder import ContextBuilder


class QueryEngine:
    def __init__(self):
        self.context_builder = ContextBuilder()
        print("QueryEngine initialized")

    def search(self, query: str, top_k: int = 5):
     return self.context_builder.build_context(
        query=query,
        top_k=top_k,
        filters=None  
    )



if __name__ == "__main__":
    qe = QueryEngine()

    while True:
        query = input("\n🔍 Enter query (or type 'exit'): ").strip()
        if query.lower() == "exit":
            print("Exiting Query Engine")
            break

        result = qe.search(query)

        print("\nCONTEXT")
        print("-" * 50)
        print(result["context"])

        print("\n SOURCES")
        print("-" * 50)
        for src in result["sources"]:
            print(
                f"Chunk ID: {src['chunk_id']} | "
                f"Source: {src['source']} | "
                f"Page: {src['page']}"
            )
