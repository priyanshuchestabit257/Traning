import ollama

SYSTEM_PROMPT = """
You are a senior data engineer.
Generate ONLY valid SQLite SQL.

Rules:
- Use only provided tables and columns
- Only SELECT queries
- No explanations, output SQL only
"""

def generate_sql(question, schema):
    schema_text = "\n".join(
        f"{table}: {', '.join(columns)}"
        for table, columns in schema.items()
    )

    prompt = f"""
Database schema:
{schema_text}

User question:
{question}
"""

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()
