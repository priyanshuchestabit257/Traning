from autogen_agentchat.agents import AssistantAgent

def create_research_agent(model_client):
    return AssistantAgent(
        name="ResearchAgent",
        model_client=model_client,
        description="Gathers factual and structured information.",
        system_message="""
You are a Research Agent.

ROLE:
- Collect factual, detailed, structured information.
- Do NOT summarize.
- Do NOT provide final answers.
- Do NOT greet or add extra commentary.
- Provide only research findings.

STRICT SEPARATION:
You are not allowed to summarize or conclude.
Memory window = 10.
"""
    )