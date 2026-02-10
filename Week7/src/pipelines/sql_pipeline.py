import sqlite3
import pandas as pd

from ..utils.schema_loader import load_schema
from ..utils.sql_validator import validate_sql
from ..generator.sql_generator import generate_sql

DB_PATH = "src/data/sql/customers.db"


def execute_sql(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def sql_qa(question: str) -> pd.DataFrame:
    schema = load_schema(DB_PATH)

    raw_sql = generate_sql(question, schema)

    print("\nGenerated SQL:")
    print("-" * 40)
    print(raw_sql.strip())
    print("-" * 40)

    sql = validate_sql(raw_sql)
    df = execute_sql(sql)
    return df


if __name__ == "__main__":
    print("\nSQL Question Answering System")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask your question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("\nExiting. Goodbye!")
            break

        if not question:
            print("Please enter a valid question.\n")
            continue

        try:
            result_df = sql_qa(question)

            print("\nResult Table:")
            print("-" * 40)

            if result_df.empty:
                print("No rows returned.")
            else:
                print(result_df.to_string(index=False))

            print("-" * 40 + "\n")

        except Exception as e:
            print("\nError:", e, "\n")
