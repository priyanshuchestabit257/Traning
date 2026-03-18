## Project Overview

This project implements a **Multi-Agent Tool Orchestration System** where an intelligent **Planner Agent** dynamically decides how to solve a user task by routing it to specialized tool agents such as:

* File Agent (filesystem operations)
* Database Agent (SQLite + SQL reasoning)
* Code Agent (Python execution & analytics)
* Answer Agent (grounded final response)

The system supports **multi-step reasoning, context passing, automation, and real execution of tools.**

---

## High Level Architecture

```
User Query
   ↓
Planner Agent (Task Decomposition)
   ↓
Orchestrator (Execution Controller)
   ↓
Tool Agents (File | DB | Code)
   ↓
Context Aggregation / Memory
   ↓
Answer Agent (Final User Response)
```

---

## Core Components

### Planner Agent — Brain of System

**Responsibilities**

* Understand user intent
* Break task into ordered execution steps
* Decide which tool agent to use
* Generate STRICT JSON execution plan

*

### Orchestrator — Execution Manager

**Responsibilities**

* Calls planner agent
* Parses execution plan
* Runs tool agents sequentially
* Maintains execution context
* Handles step failures
* Summarizes outputs

**Execution Loop**

```
for each step:
   prepare context
   execute tool
   store output
```

---

## Tool Agents

---

### File Agent

**Capabilities**

* Locate files in project
* List directories
* Read file contents
* Write / append files

**Typical Tasks**

* Find dataset
* Show file content
* Create notes.txt


### Database Agent (SQLite)

**Capabilities**

* Discover tables
* Inspect schema
* Execute SELECT queries

**Reasoning Flow**

```
list_tables → get_schema → run_query
```



### Code Execution Agent

**Capabilities**

* Execute Python scripts
* Generate synthetic datasets
* Perform pandas analytics
* Return execution logs


## Project Outcome

A **functional multi-agent automation system** capable of:

* File discovery
* Database analytics
* Python execution
* Data pipeline automation
* Insight generation
* Autonomous task decomposition

---