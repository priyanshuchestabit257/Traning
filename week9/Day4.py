from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

# initialize memories
session = SessionMemory()
vector = VectorStore()
long_term = LongTermMemory()

print("\nAI Memory System Started (type 'exit' to stop)\n")

while True:

    # user input
    query = input("User: ")

    if query.lower() == "exit":
        break

    # store user message
    session.add_message("user", query)

    # search vector memory
    similar_context = vector.search(query)

    print("\nRetrieved Memory:", similar_context)

    # simple simulated AI response
    answer = f"I understand your question about: {query}"

    # store assistant message
    session.add_message("assistant", answer)

    print("Assistant:", answer)

    # store into vector memory
    vector.add_memory(query)
    vector.add_memory(answer)

    # store into long-term memory
    long_term.store(query)
    long_term.store(answer)

    print("\nSession Memory:", session.get_memory())