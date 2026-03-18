import sys
from pathlib import Path
import os
import requests
import ollama 

from src.retriever.faiss_retriever import retrieve
from src.retriever.image_search import (
    text_to_image,
    image_to_image,
    image_to_text_answer,
    image_paths
)
from src.pipelines.sql_pipeline import sql_qa
from src.evaluation.rag_eval import faithfulness_score, hallucination_detected

SIMILARITY_THRESHOLD = 0.25

# -----------------------------
# TEXT → TEXT (RAG)
# -----------------------------
def ask_text(question):
    try:
        # 1. Get Context
        context, similarity = retrieve(question)

        # 2. Threshold Check
        if similarity < SIMILARITY_THRESHOLD or not context.strip():
            return "Information not found in the current documents.", float(similarity)

        
        system_instructions = (
            
    "You are a financial analyst. Use the provided context to answer the question. "
    "If the context provides a definition or a specific calculation for a term, "
    "explain it clearly. If the information is truly missing, say you don't know."
)
        
        
        prompt = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"

        response = ollama.generate(
            model='phi3', 
            system=system_instructions,
            prompt=prompt
        )
        answer = response['response'].strip()

        # 4. Hallucination Guard
        faith = faithfulness_score(answer, context)
        hallucination = hallucination_detected(answer, context)

        if hallucination:
            print("LOG: LLM generated content not present in source context.")
            return f"Refined Answer (Low Confidence): {answer}", 0.0

        confidence = round((float(similarity) + float(faith)) / 2, 2)
        
        return str(answer), confidence

    except Exception as e:
        print(f"Text QA Error: {e}")
        return f"System Error: {str(e)}", 0.0
# -----------------------------
# TEXT → IMAGE
# -----------------------------
def ask_image(query):
    try:
        indices, scores = text_to_image(query)
        idx = indices[0]
        similarity = float(scores[idx])
        image_path = image_paths[idx]

        if similarity < 0.2:
            return "No relevant image found in dataset.", 0.0

        # Returning formatted string so dashboard can parse the "Path:"
        return f"Top Matching Image:\nPath: {image_path}", round(similarity, 2)
    except Exception as e:
        return f"Image search error: {str(e)}", 0.0

# -----------------------------
# IMAGE → IMAGE
# -----------------------------
def ask_image_to_image(image_path):
    try:
        indices, scores = image_to_image(image_path)
        results = [f"{image_paths[i]} (score={round(float(scores[i]), 2)})" for i in indices]
        return "\n".join(results), 0.9
    except Exception as e:
        return f"Image search error: {str(e)}", 0.0

# -----------------------------
# IMAGE → TEXT
# -----------------------------
def ask_image_to_text(image_path):
    try:
        answer = image_to_text_answer(image_path)
        return str(answer), 0.9
    except Exception as e:
        return f"Image processing error: {str(e)}", 0.0

# -----------------------------
# SQL → ANSWER (Optimized for Streamlit)
# -----------------------------
def ask_sql(query):
    try:
        # This calls your sql_pipeline.py which likely uses Phi-3
        df = sql_qa(query)

        if df is None or (hasattr(df, 'empty') and df.empty):
            return "No data found for this query.", 0.0

        # If it's a single value (e.g., "SELECT COUNT(*)"), return just the value
        if df.shape == (1, 1):
            return str(df.iloc[0, 0]), 0.9
            
        # Convert DataFrame to string for the 'st.code' block in dashboard
        return df.to_string(index=False), 0.9

    except Exception as e:
        # Captures the "model not found" or "connection" errors
        error_msg = str(e)
        print(f"--- SQL ERROR LOGGED ---\n{error_msg}")
        return f"SQL Error: {error_msg}", 0.0

# -----------------------------
# CLI INTERFACE (Kept for your manual testing)
# -----------------------------
if __name__ == "__main__":
    # Your existing while True loop logic goes here if you still want to run it via terminal
    pass