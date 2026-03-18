import asyncio
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient

from agents.research_agent import create_research_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.answer_agent import create_answer_agent


async def main():

    model = LlamaCppChatCompletionClient(
        model_path="/home/priyanshurajchauhan/Desktop/Traning/week9/model/Phi-3-mini-4k-instruct-Q4_K_M.gguf",
        temperature=0.2,
        max_tokens=1024,
        context_window=4096,
        verbose=False  
    )

    research_agent = create_research_agent(model)
    summarizer_agent = create_summarizer_agent(model)
    answer_agent = create_answer_agent(model)

    user_query = input("User: ")

    # Research
    research = await research_agent.run(task=user_query)
    research_output = research.messages[-1].content
    print("\n--- Research Output ---\n")
    print(research_output)

    # Summary
    summary = await summarizer_agent.run(task=research_output)
    summary_output = summary.messages[-1].content
    print("\n--- Summary Output ---\n")
    print(summary_output)

    # Final Answer
    answer = await answer_agent.run(task=summary_output)
    final_output = answer.messages[-1].content
    print("\n--- Final Answer ---\n")
    print(final_output)


if __name__ == "__main__":
    asyncio.run(main())