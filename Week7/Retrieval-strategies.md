#  DAY 2 — Advanced Retrieval & Context Engineering

## Overview

Day 2 focuses on improving retrieval accuracy and reducing hallucinations in a Retrieval-Augmented Generation (RAG) system.  
The goal is to move beyond simple vector search and design a **hybrid, traceable, and controllable retrieval pipeline**.

This day builds on the Day-1 ingestion pipeline and introduces **context engineering** as a first-class concern.

---

## Learning Objectives

- Improve retrieval precision
- Combine semantic and keyword-based search
- Apply reranking and deduplication
- Build LLM-ready context
- Reduce hallucinations
- Ensure full source traceability

---

## System Architecture

```text
QueryEngine
   ↓
ContextBuilder
   ↓
HybridRetriever
   ↓
FAISS (semantic) + BM25 (keyword)
   ↓
Reranking + Deduplication
   ↓
Final Context (LLM-ready)
```

---

## Core Components

### 1. Hybrid Retriever

**Purpose:**  
Combine strengths of semantic and lexical search.

**Techniques used:**
- Semantic search using FAISS + embeddings (BGE model)
- Keyword fallback using BM25
- Automatic fallback when semantic recall is low

**Why hybrid search?**
- Semantic search misses exact terms
- Keyword search misses intent
- Hybrid search improves recall and precision

---

### 2. Reranking Strategy

**Purpose:**  
Improve ranking quality after initial retrieval.

**Approaches supported:**
- Cosine similarity reranking
- (Extensible to cross-encoder reranking)

**Benefits:**
- Promotes more relevant chunks
- Pushes noisy chunks down
- Improves answer grounding

---

### 3. Chunk Deduplication

**Purpose:**  
Avoid repeated or overlapping information in context.

**Strategy:**
- Hash or similarity-based deduplication
- Removes near-duplicate chunks

**Why this matters:**
- Reduces wasted context window
- Prevents repetitive LLM answers

---

### 4. Context Builder

**Purpose:**  
Convert retrieved chunks into **LLM-friendly context**.

**Responsibilities:**
- Assemble final context text
- Preserve ordering
- Attach metadata for traceability

**Output format:**
```json
{
  "context": "chunked text...",
  "sources": [
    {
      "chunk_id": 12,
      "source": "document.pdf",
      "page": 3
    }
  ]
}
```

---

### 5. Metadata Filtering

**Purpose:**  
Enable domain-specific retrieval.

**Example:**
```python
filters = {
  "year": "2024",
  "type": "policy"
}
```

**Important Note:**  
Filters only work if metadata is injected during ingestion.

---

## Hallucination Reduction Techniques

| Technique | Effect |
|---------|--------|
| Hybrid retrieval | Higher recall |
| Reranking | Better relevance |
| Deduplication | Less repetition |
| Context limits | Prevent noise |
| Source tracking | Grounded answers |

---

## Example Query

```python
query = "Explain how credit underwriting works"

context = build_context(
    query=query,
    top_k=5,
    filters=None
)
```

---

## How to Run (Day 2)

### Run Context Builder
```bash
python -m src.pipelines.context_builder
```

### Run Query Engine
```bash
python -m src.retriever.query_engine
```

---

## Deliverables Completed

- retriever/hybrid_retriever.py
- retriever/reranker.py
- pipelines/context_builder.py
- retriever/query_engine.py
- RETRIEVAL-STRATEGIES.md

---

## Key Takeaways

- FAISS is not the query engine in advanced RAG
- Context engineering is as important as retrieval
- Hybrid search significantly improves accuracy
- Traceability is essential for trust and debugging
- Modular design enables easy upgrades (MMR, cross-encoders)

---


