import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from PIL import Image
import os

from src.deployment.app import ask_text, ask_image, ask_sql



st.set_page_config(page_title="Capstone AI System", layout="wide")

st.title("Day 5 Capstone System")
st.markdown("Multi-Modal AI: Text | Image | SQL")

# Sidebar mode selection
mode = st.sidebar.radio(
    "Select Mode",
    ["Text QA", "Image QA", "SQL QA"]
)

query = st.text_input("Enter your question")

if st.button("Submit"):

    if not query:
        st.warning("Please enter a question.")
    else:

        # TEXT QA
        if mode == "Text QA":
            answer, confidence = ask_text(query)

            st.subheader("Answer")
            st.write(answer)

            st.metric("Confidence", confidence)

        # IMAGE QA
        elif mode == "Image QA":
            answer, confidence = ask_image(query)

            st.subheader("🖼 Image Result")
            st.write(answer)

            # Extract image path from answer
            lines = answer.split("\n")
            image_path = None

            for line in lines:
                if line.strip().startswith("Path:"):
                    image_path = line.replace("Path:", "").strip()

            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption=image_path, use_column_width=True)

            st.metric("Similarity Score", confidence)

        # SQL QA
        elif mode == "SQL QA":
            answer, confidence = ask_sql(query)

            st.subheader("🗄 SQL Result")
            st.write(answer)

            st.metric("Confidence", confidence)
