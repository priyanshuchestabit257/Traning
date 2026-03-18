## Overview

This project implements a **multi-layer cognitive memory system** for conversational AI agents.

The system enables the agent to:

* Remember user facts across sessions
* Perform semantic recall
* Maintain short-term conversational context
* Persist structured knowledge in a database

---

# Memory Architecture

```
User Query
   │
   ▼
Session Memory (Short Term)
   │
   ▼
Vector Semantic Search (FAISS)
   │
   ▼
Long Term Memory Fetch (SQLite)
   │
   ▼
Context Injection → LLM Response
   │
   ▼
Fact Extraction → Memory Update
```

---

# Memory Layers

## 1. Session Memory (Short-Term Memory)

File: `session_memory.py`

### Purpose

* Stores recent conversation messages
* Maintains conversational continuity
* Helps LLM understand dialogue flow


## 2. Vector Store (Semantic Memory)

File: `vector_store.py`

### Purpose

* Enables semantic similarity search
* Retrieves relevant memories even when wording differs

### Technology

* FAISS IndexFlatIP
* SentenceTransformers model: `all-MiniLM-L6-v2`
* Cosine similarity via normalized embeddings

### Flow

```
Fact Text
   ↓
Embedding
   ↓
Stored in FAISS
   ↓
Similarity Search during retrieval
```

### Features

* Persistent semantic index
* Safe rebuild on delete
* Backward-compatible metadata loading
* String UUID memory IDs
* Normalized vector scoring

---

## 3. Long-Term Memory (Persistent Knowledge Store)

File: `long_term_memory.py`


### Purpose

* Stores structured user facts permanently
* Supports identity memory and importance ranking

### Database

SQLite database file:

```
customers.db
```
