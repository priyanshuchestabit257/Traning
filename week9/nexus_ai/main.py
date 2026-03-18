

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
from nexus_ai.memory.agent_memory import AgentMemorySystem


async def main():

    print("\nMulti-Agent System (Local Phi-3)\n")

    # -------------------------------
    # Load Local Model
    # -------------------------------

    base_path = os.path.dirname(os.path.abspath(__file__))
    model_filename = "Phi-3-mini-4k-instruct-Q4_K_M.gguf"
    model_path = "/home/priyanshurajchauhan/Desktop/Traning/week9/model/Phi-3-mini-4k-instruct-Q4_K_M.gguf"

    model_client = LlamaCppChatCompletionClient(
        model_path=model_path,
        n_ctx=4096,
        temperature=0.2,
        n_threads=os.cpu_count(),
    )

    # -------------------------------
    # Memory System
    # -------------------------------

    memory_system = AgentMemorySystem(
        session_max_turns=50,
        vector_k=5,
        vector_threshold=0.3,
        db_path="nexus_ai/datastore/agent_long_term.db",
        vector_persist_path="nexus_ai/datastore/agent_vectors.faiss"
    )

    # -------------------------------
    # Initialize Agents
    # -------------------------------

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

    # -------------------------------
    # Orchestrator
    # -------------------------------

    orchestrator = MemoryEnabledOrchestrator(
        planner_agent=planner,
        agents_dict=agents,
        memory_system=memory_system
    )

    # -------------------------------
    # Tasks
    # -------------------------------

    tasks = [
        "What did we discuss last time?"
    ]

    for task in tasks:

        result = await orchestrator.execute(task, use_memory=True)

        print("\n" + "=" * 70)
        print("FINAL OUTPUT")
        print("=" * 70)
        print(result)
        print("=" * 70)

        stats = await orchestrator.get_memory_stats()
        print(f"\nMemory Stats: {stats}\n")

    await memory_system.close()


if __name__ == "__main__":
    asyncio.run(main())

