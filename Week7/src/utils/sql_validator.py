import re

def validate_sql(sql: str):
    # Remove markdown code fences if present
    sql = re.sub(r"```sql|```", "", sql, flags=re.IGNORECASE).strip()

    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    forbidden = ["insert", "update", "delete", "drop", "alter"]
    for word in forbidden:
        if word in sql.lower():
            raise ValueError(f"Forbidden SQL keyword detected: {word}")

    return sql
