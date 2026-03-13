import asyncio
import os
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient

# Import your custom agents/tools
from tools.file_executor import file_executor
from tools.db_executor import db_agent
from tools.code_executor import code_executor

async def main():
    # 1. Setup Absolute Paths for the Local Model
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_filename = "Phi-3-mini-4k-instruct-Q4_K_M.gguf"
    model_path = os.path.join(base_path, "model", model_filename)
    
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        return

    print(f"--- Loading Local Model: {model_filename} ---")
    
    # Initialize the local client
    client = LlamaCppChatCompletionClient(
        model_path=model_path,
        n_ctx=4096,
        verbose=False
    )

    # 2. Initialize the DB Agent (Specialist)
    customer_db_agent = db_agent(name="DB_Specialist", model_client=client)

    print("\n=========================================")
    print("--- DAY 3: MULTI-AGENT LOCAL SYSTEM ---")
    print("=========================================\n")

    while True:
        try:
            user_query = input("User Request (or 'exit'): ")
            if user_query.lower() in ["exit", "quit"]:
                break
            if not user_query.strip():
                continue

            query_lower = user_query.lower()

            # --- ROUTING LOGIC (STRICT INDENTATION) ---

            # A. Check DB Keywords
            db_keywords = ["db", "customer", "table", "sql", "data", "select", "insert"]
            if any(word in query_lower for word in db_keywords):
                print("\n[Action] Routing to DB Agent...")
                result = await customer_db_agent.run(task=user_query)
                final_response = result.messages[-1].content

            # B. Check Code Keywords
            elif any(word in query_lower for word in ["code", "script", "factorial", "calculate", "python", "math", "def "]):
                print("\n[Action] Routing to Code Agent...")
                final_response = await code_executor(user_query, client)

            # C. Check File Keywords
            elif any(word in query_lower for word in ["file", "directory", "folder", "list files", "ls"]):
                print("\n[Action] Routing to File Agent...")
                final_response = await file_executor(user_query, client)

            # D. Fallback to General Reasoning
            else:
                print("\n[Action] General Reasoning...")
                # Raw dictionary for LlamaCpp compatibility
                raw_msg = {"role": "user", "content": user_query}
                response = await client.create(messages=[raw_msg])
                final_response = response.content

            print(f"\n[Response]: {final_response}\n" + "-"*50)

        except Exception as e:
            print(f"\n[System Error]: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())