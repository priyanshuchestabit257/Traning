from autogen_agentchat.agents import AssistantAgent

def create_answer_agent(model_client):
    return AssistantAgent(
        name="AnswerAgent",
        model_client=model_client,
        description="Produces the final clear answer.",
        system_message="""
You are an Answer Agent.

ROLE:
- Convert summary into final clear answer.
- Be structured and professional.
- Do NOT introduce new facts.
- If summary is insufficient, state that clearly.
- No greetings or extra commentary.

STRICT SEPARATION:
You only produce the final answer.
Memory window = 10.
"""
    )