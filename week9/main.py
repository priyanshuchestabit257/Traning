import asyncio
import os
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from orchestrator.planner_agent import Planner

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = "/home/priyanshurajchauhan/Desktop/Traning/week9/model/Phi-3-mini-4k-instruct-Q4_K_M.gguf"

    model_client = LlamaCppChatCompletionClient(
        model_path=model_path,
        temperature=0.2,
        n_ctx=4096,
        verbose=False,
    )

    planner = Planner(model_client)
    
    user_query = input("User Query: ")
    
    print("\n--- Orchestrating Task DAG ---")
    final_answer, execution_tree = await planner.run(user_query)

    print("\n--- EXECUTION TREE ---")
    for node_id, data in execution_tree.items():
        print(f"[{node_id}] Role: {data['role']} | Deps: {data['deps']}")
    
    print("\n--- FINAL VALIDATED ANSWER ---")
    print(final_answer)

if __name__ == "__main__":
    asyncio.run(main())