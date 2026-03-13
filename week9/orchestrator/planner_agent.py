import asyncio
import json
from typing import List, Literal, Dict, Any

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from pydantic import BaseModel, ValidationError, field_validator

# Assuming these are defined in your project structure
from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectorAgent
from agents.validator_agent import ValidatorAgent

def extract_json_object(text: str) -> str:
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError("Unbalanced JSON braces")

planner_msg = """
You are a planning agent. Your ONLY job is to output a JSON object describing a task DAG.

STRICT RULES:
- Output ONLY valid JSON. No markdown, no backticks, no explanations.
- Every 'id' must be unique.
- Every item in 'deps' MUST match an 'id' of a PREVIOUS node in the list.
- Do NOT include external data sources (like 'raw_data') in 'deps'. 
- If a node has no dependencies, 'deps' must be an empty list [].
- The DAG must contain at least one worker and exactly one validator.
- The validator MUST be the final node and depend on at least one other node.

JSON SCHEMA:
{
  "nodes": [
    {
      "id": "string",
      "role": "worker" | "reflector" | "validator",
      "task": "string",
      "deps": ["string"]
    }
  ]
}
"""

class DAGNode(BaseModel):
    id: str
    role: Literal["worker", "reflector", "validator"]
    task: str
    deps: List[str]

    @field_validator("id")
    @classmethod
    def id_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("id must be non-empty")
        return v

class Planner:
    def __init__(self, model_client):
        self.model_client = model_client
        self.execution_tree = {}

        self.planner_agent = AssistantAgent(
            name="planner",
            system_message=planner_msg,
            model_client=model_client,
        )

    def _validate_dag(self, nodes: List[DAGNode]) -> None:
        ids = {n.id for n in nodes}
        for node in nodes:
            for dep in node.deps:
                if dep not in ids:
                    raise ValueError(
                        f"Node '{node.id}' depends on unknown node '{dep}'. "
                        f"Ensure 'deps' only contains IDs from the node list."
                    )

        validators = [n for n in nodes if n.role == "validator"]
        if len(validators) != 1:
            raise ValueError("DAG must contain exactly one validator node")

        if not validators[0].deps:
            raise ValueError("Validator must have at least one dependency to check")

    async def create_plan(self, query: str) -> List[DAGNode]:
        cancellation = CancellationToken()
        response = await self.planner_agent.on_messages(
            [TextMessage(content=query, source="user")],
            cancellation
        )
        output = response.chat_message.content
        
        try:
            json_text = extract_json_object(output)
            raw = json.loads(json_text)
            nodes = [DAGNode(**n) for n in raw.get("nodes", [])]
            self._validate_dag(nodes)
            return nodes
        except (json.JSONDecodeError, KeyError, ValidationError, ValueError) as e:
            # Fallback/Debug: Print the raw output if it fails
            print(f"DEBUG: Planner output was: {output}")
            raise RuntimeError(f"Invalid DAG generated: {e}")

    async def run(self, query: str):
        nodes = await self.create_plan(query)
        results = {}
        pending = {n.id: n for n in nodes}

        

        while pending:
            # Nodes are ready if all their dependencies are already in 'results'
            ready = [
                n for n in pending.values()
                if all(dep in results for dep in n.deps)
            ]

            if not ready:
                raise RuntimeError("Cyclic dependency detected or invalid DAG structure.")

            tasks = []
            for node in ready:
                if node.role == "worker":
                    agent = WorkerAgent(node.id, node.task, self.model_client)
                    tasks.append(self._run_worker(agent, node, query))
                elif node.role == "reflector":
                    agent = ReflectorAgent(self.model_client)
                    inputs = [results[d] for d in node.deps]
                    tasks.append(self._run_reflector(agent, node, inputs))
                elif node.role == "validator":
                    agent = ValidatorAgent(self.model_client)
                    # Validators typically check the last thing produced
                    input_text = results[node.deps[0]]
                    tasks.append(self._run_validator(agent, node, input_text))

            outputs = await asyncio.gather(*tasks)
            
            for node_id, output in outputs:
                results[node_id] = output
                self.execution_tree[node_id] = {
                    "role": pending[node_id].role,
                    "deps": pending[node_id].deps,
                    "output": output,
                }
                del pending[node_id]

        # Return the output of the Validator node as the final answer
        final_node_id = next(n.id for n in nodes if n.role == "validator")
        return results[final_node_id], self.execution_tree

    async def _run_worker(self, agent, node: DAGNode, query: str):
        # Adjusted to match common Agent return patterns
        resp = await agent.run(query)
        return node.id, resp.get("output", str(resp))

    async def _run_reflector(self, agent, node: DAGNode, inputs: List[str]):
        resp = await agent.run(inputs)
        return node.id, resp

    async def _run_validator(self, agent, node: DAGNode, input_text: str):
        resp = await agent.run(input_text)
        return node.id, resp