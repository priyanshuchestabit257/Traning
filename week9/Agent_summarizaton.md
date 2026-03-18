## Overview

This project demonstrates a basic **Agentic AI pipeline** using Microsoft AutoGen.
The system consists of three specialized agents working together through structured message passing.

**Architecture Flow**

User → ResearchAgent → SummarizerAgent → AnswerAgent

Each agent has a clearly defined role and operates under strict separation of responsibilities.

---

## Core Concepts

### Agentic Loop

All agents follow the same internal cycle:

Perception → Reasoning → Action

* **Perception** — Reads incoming messages and context
* **Reasoning** — Applies system prompt and role rules
* **Action** — Generates response using the model

---

## Role-Based Design

Agents are built with strict job boundaries to maintain clarity and scalability.

### ResearchAgent

**Purpose**

* Collect factual research notes

**Role**

* Collect factual, detailed, structured information.
* Do NOT summarize.
* Do NOT provide final answers.
* Do NOT greet or add extra commentary.
* Provide only research findings.

---

### SummarizerAgent

**Purpose**

* Compress research into a structured summary

**Role**

*  Convert research into a concise summary.
* Summary MUST be shorter than research.
* Remove repetition.
* Do NOT add new information.
* Do NOT answer the user directly.

---

### AnswerAgent

**Purpose**

* Produce final user-ready explanation

**Role**

* Convert summary into final clear answer.
* Be structured and professional.
* Do NOT introduce new facts.
* If summary is insufficient, state that clearly.
* No greetings or extra commentary.





