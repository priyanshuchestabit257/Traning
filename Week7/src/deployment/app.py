from src.retriever.faiss_retriever import retrieve
from src.retriever.image_search import (
    text_to_image,
    image_to_image,
    image_to_text_answer,
    image_paths
)
from src.pipelines.sql_pipeline import sql_qa
from src.evaluation.rag_eval import faithfulness_score, hallucination_detected


SIMILARITY_THRESHOLD = 0.65


# -----------------------------
# TEXT → TEXT (RAG)
# -----------------------------
def ask_text(question):
    context, similarity = retrieve(question)

    if similarity < SIMILARITY_THRESHOLD or not context.strip():
        return "Answer not found in provided documents.", 0.0

    sentences = context.split(".")
    relevant_sentences = []

    for sentence in sentences:
        if any(word.lower() in sentence.lower() for word in question.split()):
            relevant_sentences.append(sentence.strip())

    if not relevant_sentences:
        answer = context.strip()
    else:
        answer = ". ".join(relevant_sentences) + "."

    faith = faithfulness_score(answer, context)
    hallucination = hallucination_detected(answer, context)

    if hallucination:
        return "Answer rejected due to hallucination risk.", 0.0

    confidence = round((similarity + faith) / 2, 2)

    return answer.strip(), confidence


# -----------------------------
# TEXT → IMAGE
# -----------------------------
def ask_image(query):
    indices, scores = text_to_image(query)

    idx = indices[0]
    similarity = float(scores[idx])
    image_path = image_paths[idx]

    if similarity < 0.2:
        return "No relevant image found in dataset.", 0.0

    return f"Top Matching Image:\nPath: {image_path}", round(similarity, 2)


# -----------------------------
# IMAGE → IMAGE
# -----------------------------
def ask_image_to_image(image_path):
    try:
        indices, scores = image_to_image(image_path)

        results = []
        for i in indices:
            path = image_paths[i]
            score = float(scores[i])
            results.append(f"{path} (score={round(score,2)})")

        return "\n".join(results), 0.9

    except Exception as e:
        return f"Image search error: {str(e)}", 0.0


# -----------------------------
# IMAGE → TEXT (Caption + OCR)
# -----------------------------
def ask_image_to_text(image_path):
    try:
        answer = image_to_text_answer(image_path)
        return answer, 0.9

    except Exception as e:
        return f"Image processing error: {str(e)}", 0.0


# -----------------------------
# SQL → ANSWER
# -----------------------------
def ask_sql(query):
    try:
        df = sql_qa(query)

        if df.empty:
            return "No rows returned.", 0.0

        return df.to_string(index=False), 0.9

    except Exception as e:
        return f"SQL Error: {str(e)}", 0.0


# -----------------------------
# CLI INTERFACE
# -----------------------------
if __name__ == "__main__":
    print("Day 5 Capstone System")
    print(
        "Modes:\n"
        "/ask <question>\n"
        "/ask-image <text>\n"
        "/image-search <image_path>\n"
        "/image-to-text <image_path>\n"
        "/ask-sql <query>\n"
        "exit\n"
    )

    while True:
        cmd = input("Enter command: ")

        if cmd == "exit":
            break

        if cmd.startswith("/ask "):
            q = cmd.replace("/ask ", "")
            ans, conf = ask_text(q)

        elif cmd.startswith("/ask-image "):
            q = cmd.replace("/ask-image ", "")
            ans, conf = ask_image(q)

        elif cmd.startswith("/image-search "):
            path = cmd.replace("/image-search ", "")
            ans, conf = ask_image_to_image(path)

        elif cmd.startswith("/image-to-text "):
            path = cmd.replace("/image-to-text ", "")
            ans, conf = ask_image_to_text(path)

        elif cmd.startswith("/ask-sql "):
            q = cmd.replace("/ask-sql ", "")
            ans, conf = ask_sql(q)

        else:
            print("Invalid command.\n")
            continue

        print("\nAnswer:\n")
        print(ans)
        print(f"\nConfidence: {conf}\n")