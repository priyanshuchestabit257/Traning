import os
import asyncio
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.messages import ToolCallSummaryMessage
from autogen_agentchat.agents import AssistantAgent

async def code_executor(input_query: str, model_client):
    """
    Day 3 Tool: Executes Python code locally using the LlamaCpp client.
    """
    # 1. Ensure the work directory exists
    work_dir = "src"
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    # 2. Setup the Local Executor and Tool
    # Timeout set to 60 seconds (usually enough for local tasks)
    executor = LocalCommandLineCodeExecutor(work_dir=work_dir, timeout=60)
    tool = PythonCodeExecutionTool(executor)
    
    # 3. Initialize the Agent with your local model_client (Phi-3)
    agent = AssistantAgent(
        name="coding_assistant",
        tools=[tool],
        model_client=model_client,
        max_tool_iterations=5, # Limit loops to prevent local model hanging
        system_message=(
            "You are a code executor. "
            "To solve tasks, write a Python script and execute it using the tool. "
            "The script must perform the computation and use print() for output. "
            "Do not just state the answer; run the code to verify it."
        )
    )
    
    # 4. Run the task
    result = await agent.run(task=input_query)
    
    # 5. Extract the output from the tool execution
    for msg in reversed(result.messages):
        if isinstance(msg, ToolCallSummaryMessage):
            return f"Code Execution Result:\n{msg.content}"
            
    # Fallback to the last text message if no tool summary is found
    return result.messages[-1].content