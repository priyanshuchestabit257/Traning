import asyncio

from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from memory.long_term_memory import LongTermMemory

from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from autogen_core.models import UserMessage

session = SessionMemory()
vector = VectorStore()
long_term = LongTermMemory()

llm = LlamaCppChatCompletionClient(
    model_path="/home/priyanshurajchauhan/Desktop/Traning/week9/model/Phi-3-mini-4k-instruct-Q4_K_M.gguf",
    temperature=0.7,
    max_tokens=512,
    verbose=False
)


async def main():

    print("\nAI Memory Agent Started (type 'exit' to stop)\n")

    while True:
        query = input("User: ")

        if query.lower() == "exit":
            break

        session.add_message("user", query)

        long_term_data = long_term.fetch_all()[-5:]
        similar_context = vector.search(query)
        past_convo = session.get_memory()

        prompt = f"""
You are a helpful AI assistant with persistent memory.

Conversation History:
{past_convo}

Relevant Memory:
{similar_context}

Long-Term Memory:
{long_term_data}

Rules:
- You DO remember user information across sessions
- Do Not Print any Note in between
- NEVER say you forget after the chat ends
- NEVER give generic AI disclaimers
- Only use memory when relevant


User: {query}
Assistant:
"""

        response = await llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        answer = response.content

        session.add_message("assistant", answer)

        print("\nAssistant:", answer)

        vector.add_memory(query)
        vector.add_memory(answer)

        long_term.store(query)
        long_term.store(answer)


if __name__ == "__main__":
    asyncio.run(main())