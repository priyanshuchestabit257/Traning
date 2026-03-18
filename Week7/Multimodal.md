## 1. Overview

This document describes the implementation of a **Multimodal Retrieval-Augmented Generation (RAG)** system that supports:

- 📄 Text → Text Retrieval

- 📄 Text → Image Retrieval

- 🖼 Image → Image Retrieval

- 🖼 Image → Text Retrieval (via Captioning)

The system dynamically routes user input based on modality (text or image) and ensures traceable, low-hallucination retrieval.

## 2. High-Level Architecture
```css
User Input
   |
   ├── Text Input
   |     ├── Text → Text (FAISS + BGE)
   |     └── Text → Image (CLIP)
   |
   └── Image Input
         ├── Image → Image (CLIP)
         └── Image → Caption → Text (BLIP → BGE → FAISS)
```
## 3. Models & Techniques Summary

| Component            | Technique            | Model / Tool                              |
|---------------------|----------------------|-------------------------------------------|
| Text Embeddings     | Dense embeddings     | BAAI/bge-small-en                         |
| Image Embeddings    | Vision-language      | openai/clip-vit-base-patch32              |
| Image Captioning    | Vision → Text        | Salesforce/blip-image-captioning-base     |
| Vector Search       | ANN                  | FAISS                                     |
| Multimodal Routing  | Rule-based           | Python Router                             |
| Traceability        | Metadata             | source + chunk_id                         

### Logic

| Input Type | Actions |
|-----------|---------|
| **Text**  | Text → Text Retrieval + Text → Image Retrieval |
| **Image** | Image → Image Retrieval + Image → Caption → Text Retrieval |
