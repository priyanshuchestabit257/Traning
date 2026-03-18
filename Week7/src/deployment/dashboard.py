import sys
from pathlib import Path
import os

# Setup Pathing
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from PIL import Image
import src.deployment.app as backend

st.set_page_config(page_title="Capstone AI System", layout="wide")

st.title("Day 5 Capstone System")
st.markdown("---")

# 1. INITIALIZE VARIABLES (Prevents NameError if no block executes)
answer = "No data yet"
confidence = 0.0

# Sidebar mode selection
mode = st.sidebar.radio(
    "Select Mode",
    ["Text QA", "Text → Image", "Image → Image", "Image → Text", "SQL QA"]
)

query = st.text_input("Enter your query", key="query_input")

if st.button("Submit Query"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner(f"Processing {mode}..."):
            
            # --- TEXT QA ---
            if mode == "Text QA":
                answer, confidence = backend.ask_text(query)
                st.subheader("Text Answer")
                st.info(answer)
                st.metric("Confidence", confidence)

            # --- TEXT → IMAGE ---
            elif mode == "Text → Image":
                answer, confidence = backend.ask_image(query)
                st.subheader("Retrieved Image")
                
                # Logic to extract path from the string "Path: /your/path"
                image_path = None
                for line in answer.split("\n"):
                    if "Path:" in line:
                        image_path = line.split("Path:")[-1].strip()
                
                if image_path and os.path.exists(image_path):
                    st.image(Image.open(image_path), caption=f"Similarity: {confidence}")
                else:
                    st.warning("Found a match, but the image file path is missing or invalid.")
                    st.write(answer)
                st.metric("Similarity Score", confidence)

            # --- IMAGE → IMAGE ---
            elif mode == "Image → Image":
                answer, confidence = backend.ask_image_to_image(query)
                st.subheader("Similar Images")
                paths = answer.split("\n")
                cols = st.columns(len(paths) if len(paths) > 0 else 1)
                for i, p in enumerate(paths):
                    clean_path = p.split(" ")[0].strip()
                    if os.path.exists(clean_path):
                        with cols[i % len(cols)]:
                            st.image(Image.open(clean_path), use_container_width=True)
                            st.caption(p)
                st.metric("Confidence", confidence)

            # --- IMAGE → TEXT ---
            elif mode == "Image → Text":
                answer, confidence = backend.ask_image_to_text(query)
                st.subheader("Image Description")
                st.write(answer)
                if os.path.exists(query):
                    st.image(Image.open(query), width=300)
                st.metric("Confidence", confidence)

            # --- SQL QA ---
            elif mode == "SQL QA":
                answer, confidence = backend.ask_sql(query)
                st.subheader("SQL Results")
                st.code(answer)
                st.metric("Confidence", confidence)

# --- DEBUG SECTION ---
with st.expander("Developer Debug Logs"):
    st.write(f"Mode selected: {mode}")
    st.write(f"Raw Answer Value: {answer}")
    st.write(f"Raw Confidence: {confidence}")