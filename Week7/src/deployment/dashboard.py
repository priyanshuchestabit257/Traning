import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from PIL import Image
import os

from src.deployment.app import (
    ask_text,
    ask_image,
    ask_image_to_image,
    ask_image_to_text,
    ask_sql
)

st.set_page_config(page_title="Capstone AI System", layout="wide")

st.title("Day 5 Capstone System")
st.markdown("Multi-Modal AI: Text | Image | SQL")

# Sidebar mode selection
mode = st.sidebar.radio(
    "Select Mode",
    [
        "Text QA",
        "Text → Image",
        "Image → Image",
        "Image → Text",
        "SQL QA"
    ]
)

query = st.text_input("Enter your query")

if st.button("Submit"):

    if not query:
        st.warning("Please enter a query.")
    else:

        # TEXT QA
        if mode == "Text QA":
            answer, confidence = ask_text(query)

            st.subheader("Answer")
            st.write(answer)
            st.metric("Confidence", confidence)

        # TEXT → IMAGE
        elif mode == "Text → Image":
            answer, confidence = ask_image(query)

            st.subheader("Image Result")
            st.write(answer)

            # Extract image path
            image_path = None
            lines = answer.split("\n")

            for line in lines:
                if line.startswith("Path:"):
                    image_path = line.replace("Path:", "").strip()

            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                st.image(image, caption=image_path, use_container_width=True)

            st.metric("Similarity Score", confidence)

        # IMAGE → IMAGE
        elif mode == "Image → Image":
            answer, confidence = ask_image_to_image(query)

            st.subheader("Similar Images")

            paths = answer.split("\n")

            for p in paths:
                img_path = p.split(" ")[0]

                if os.path.exists(img_path):
                    image = Image.open(img_path)
                    st.image(image, caption=p, use_container_width=True)

            st.metric("Confidence", confidence)

        # IMAGE → TEXT
        elif mode == "Image → Text":
            answer, confidence = ask_image_to_text(query)

            st.subheader("Image Description")
            st.write(answer)

            if os.path.exists(query):
                image = Image.open(query)
                st.image(image, caption=query, use_container_width=True)

            st.metric("Confidence", confidence)

        # SQL QA
        elif mode == "SQL QA":
            answer, confidence = ask_sql(query)

            st.subheader("SQL Result")
            st.code(answer)
            st.metric("Confidence", confidence)