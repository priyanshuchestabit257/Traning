import asyncio
import os

from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient

from nexus_ai.agents.researcher_agent import ResearcherAgent
from nexus_ai.agents.analyst_agent import AnalystAgent
from nexus_ai.agents.critic_agent import CriticAgent
from nexus_ai.agents.optimizer_agent import OptimizerAgent
from nexus_ai.agents.validator_agent import ValidatorAgent
from nexus_ai.agents.reporter_agent import ReporterAgent
from nexus_ai.agents.planner_agent import PlannerAgent
from nexus_ai.agents.coder_agent import CoderAgent
from nexus_ai.agents.orchestrator import MemoryEnabledOrchestrator


async def main():
    print("\n==============================")
    print("   Multi-Agent AI System")
    print("==============================\n")

    model_path = "/home/priyanshurajchauhan/Desktop/Traning/week9/model/Phi-3-mini-4k-instruct-Q4_K_M.gguf"

    if not os.path.exists(model_path):
        print(f"Model not found at: {model_path}")
        return

    model_client = LlamaCppChatCompletionClient(
        model_path=model_path,
        n_ctx=4096,
        temperature=0.2,
        n_threads=os.cpu_count(),
        verbose=False
    )

    planner = PlannerAgent(model_client)
    researcher = ResearcherAgent(model_client)
    analyst = AnalystAgent(model_client)
    coder = CoderAgent(model_client)
    critic = CriticAgent(model_client)
    optimizer = OptimizerAgent(model_client)
    validator = ValidatorAgent(model_client)
    reporter = ReporterAgent(model_client)

    agents = {
        "Researcher": researcher,
        "Analyst": analyst,
        "Coder": coder,
        "Critic": critic,
        "Optimizer": optimizer,
        "Validator": validator,
        "Reporter": reporter
    }

    orchestrator = MemoryEnabledOrchestrator(
        planner_agent=planner,
        agents_dict=agents
    )

    
    while True:
        task = input("Enter your task (type 'exit' to quit): ").strip()

        if task.lower() == "exit":
            print("\nExiting... Goodbye!")
            break

        if not task:
            print("Please enter a valid task.\n")
            continue

        try:
            print("\nProcessing...\n")
            result = await orchestrator.execute(task)

            print("\n==============================")
            print("FINAL OUTPUT")
            print("==============================\n")
            print(result)
            print("\n" + "=" * 70 + "\n")

        except Exception as e:
            print(f"Error occurred: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())