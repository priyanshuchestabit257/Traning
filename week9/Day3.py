
import asyncio
import os
import re

from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient

from tools.code_executor import code_executor
from tools.file_executor import file_executor
from tools.db_executor import db_agent, SQLiteDBTools


def extract_sql(response_text: str):
    matches = re.findall(r'execute_query\(["\'](.+?)["\']\)', response_text)

    for sql in matches:
        if "get_db_tables" not in sql and "inspect_table_schema" not in sql:
            return sql

    raw_sql_match = re.search(r"(SELECT .*?)(?:;|\n|$)", response_text, re.IGNORECASE)

    if raw_sql_match:
        return raw_sql_match.group(1)

    return None


def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = re.sub(r"''([^']+)''", r"'\1'", sql)
    sql = sql.replace("`", "")
    return sql


async def main():

    base_path = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_path, "model", "Phi-3-mini-4k-instruct-Q4_K_M.gguf")

    if not os.path.exists(model_path):
        print("ERROR: Model not found.")
        return

    print("\n--- Loading Local Model: Phi-3-mini-4k-instruct-Q4_K_M.gguf ---")

    client = LlamaCppChatCompletionClient(
        model_path=model_path,
        n_ctx=4096,
        verbose=False
    )

    db_agent_instance = db_agent(name="DB_Specialist", model_client=client)

    db_path = "/home/priyanshurajchauhan/Desktop/Traning/Week7/src/data/sql/customers.db"
    db_tools = SQLiteDBTools(db_path)

    print("\n=========================================")
    print("---- DAY 3: MULTI AGENT LOCAL SYSTEM ----")
    print("=========================================\n")

    while True:

        try:

            user_query = input("User Request (or 'exit'): ")

            if user_query.lower() in ["exit", "quit"]:
                break

            if not user_query.strip():
                continue

            query_lower = user_query.lower()

            db_keywords = ["customer", "database", "table", "sql", "data"]
            code_keywords = ["code", "python", "script", "calculate", "factorial", "math"]
            file_keywords = ["file", "folder", "directory", "list files", "ls"]

            if any(word in query_lower for word in db_keywords):

                print("\n[Action] Routing to DB Agent...")

                result = await db_agent_instance.run(task=user_query)

                response_text = result.messages[-1].content
                response_text = response_text.replace("```sql", "").replace("```", "").strip()

                print("[Model Output]:", response_text)

                sql = extract_sql(response_text)

                if sql:
                    sql = clean_sql(sql)

                    print("\n[Executing SQL]:", sql)

                    db_result = db_tools.execute_query(sql)

                    if "rows" in db_result:

                        print("\n[Database Result]:")

                        for row in db_result["rows"]:
                            print(row)

                        print(f"\n[Returned Rows]: {db_result['row_count']}")

                    else:
                        print(db_result)

                else:
                    print("\n[Response]:", response_text)

            elif any(word in query_lower for word in code_keywords):

                print("\n[Action] Routing to Code Executor...")

                response = await code_executor(user_query, client)

                print("\n[Response]:", response)

            elif any(word in query_lower for word in file_keywords):

                print("\n[Action] Routing to File Executor...")

                response = await file_executor(user_query, client)

                print("\n[Response]:", response)

            else:

                print("\n[Action] General Reasoning...")

                messages = [{"role": "user", "content": user_query}]

                response = await client.create(messages=messages)

                if hasattr(response, "content"):
                    print("\n[Response]:", response.content)
                else:
                    print("\n[Response]:", response)

            print("\n" + "-" * 60)

        except Exception as e:
            print("\n[System Error]:", str(e))


if __name__ == "__main__":
    asyncio.run(main())

