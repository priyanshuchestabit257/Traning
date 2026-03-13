from autogen_agentchat.agents import AssistantAgent

def create_summarizer_agent(model_client):
    return AssistantAgent(
        name="SummarizerAgent",
        model_client=model_client,
        description="Condenses research into concise summaries.",
        system_message="""
You are a Summarizer Agent.

ROLE:
- Convert research into a concise summary.
- Summary MUST be shorter than research.
- Remove repetition.
- Do NOT add new information.
- Do NOT answer the user directly.

STRICT SEPARATION:
You only summarize.
Memory window = 10.
"""
    )