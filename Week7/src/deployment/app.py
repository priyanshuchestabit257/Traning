from src.retriever.faiss_retriever import retrieve
from src.retriever.image_search import text_to_image, image_paths
from src.pipelines.sql_pipeline import sql_qa
from src.evaluation.rag_eval import faithfulness_score, hallucination_detected

SIMILARITY_THRESHOLD = 0.65


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


def ask_image(query):
    indices, scores = text_to_image(query)

    idx = indices[0]
    similarity = float(scores[idx])
    image_path = image_paths[idx]

    if similarity < 0.2:
        return "No relevant image found in dataset.", 0.0

    return f"Top Matching Image:\nPath: {image_path}", round(similarity, 2)


def ask_sql(query):
    try:
        df = sql_qa(query)

        if df.empty:
            return "No rows returned.", 0.0

        return df.to_string(index=False), 0.9

    except Exception as e:
        return f"SQL Error: {str(e)}", 0.0


if __name__ == "__main__":
    print("Day 5 Capstone System")
    print("Modes: /ask | /ask-image | /ask-sql | exit\n")

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

        elif cmd.startswith("/ask-sql "):
            q = cmd.replace("/ask-sql ", "")
            ans, conf = ask_sql(q)

        else:
            print("Invalid command.\n")
            continue

        print("\nAnswer:\n")
        print(ans)
        print(f"\nConfidence: {conf}\n")
