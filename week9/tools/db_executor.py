
import sqlite3
import re
from typing import Any, Dict, List, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool


FORBIDDEN_SQL_PATTERNS = re.compile(
    r"\b(UPDATE|DELETE|DROP|ALTER|TRUNCATE|ATTACH|DETACH|PRAGMA)\b",
    re.IGNORECASE,
)

ALLOWED_WRITE_PATTERNS = re.compile(
    r"^\s*INSERT\s+INTO\b",
    re.IGNORECASE,
)

VALID_TABLE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
MAX_RETURN_ROWS = 200


def connect_db(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path, check_same_thread=False, timeout=5)


def list_tables(conn: sqlite3.Connection) -> List[str]:
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return [row[0] for row in cursor.fetchall()]


def get_table_schema(conn: sqlite3.Connection, table_names: List[str]) -> Dict[str, Any]:
    schemas = {}

    for table in table_names:
        if not VALID_TABLE.match(table):
            raise ValueError(f"Invalid table name: {table}")

        cursor = conn.execute(f'SELECT * FROM "{table}" LIMIT 0')

        schemas[table] = [
            {"column": d[0], "type": d[1]}
            for d in cursor.description
        ]

    return schemas


def validate_sql(sql: str, allow_write: bool) -> Optional[str]:
    sql_clean = sql.strip()

    if FORBIDDEN_SQL_PATTERNS.search(sql_clean):
        return "Dangerous SQL blocked"

    is_insert = bool(ALLOWED_WRITE_PATTERNS.match(sql_clean))
    is_select = sql_clean.lower().startswith("select")

    if is_insert and not allow_write:
        return "Write not permitted"

    if not (is_select or is_insert):
        return "Only SELECT and INSERT allowed"

    return None


def clean_sql(sql: str) -> str:
    sql = sql.strip()
    sql = re.sub(r"''([^']+)''", r"'\1'", sql)
    sql = sql.replace("`", "")
    return sql


def execute_sql(conn: sqlite3.Connection, sql: str) -> Dict[str, Any]:

    if "limit" not in sql.lower():
        sql = sql.strip() + f" LIMIT {MAX_RETURN_ROWS}"

    cursor = conn.execute(sql)

    if cursor.description:
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchmany(MAX_RETURN_ROWS)

        return {
            "rows": [dict(zip(columns, row)) for row in rows],
            "row_count": len(rows),
        }

    conn.commit()
    return {"rows_affected": cursor.rowcount}


class SQLiteDBTools:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_db_tables(self) -> dict:
        conn = connect_db(self.db_path)
        try:
            return {"tables": list_tables(conn)}
        finally:
            conn.close()

    def inspect_table_schema(self, table_name: str) -> dict:
        conn = connect_db(self.db_path)
        try:
            return {"schema": get_table_schema(conn, [table_name])}
        finally:
            conn.close()

    def execute_query(self, sql: str, allow_write: bool = False) -> dict:

        sql = clean_sql(sql)

        if "get_db_tables" in sql or "inspect_table_schema" in sql:
            return {"error": "Invalid SQL: tool used as table"}

        validation_error = validate_sql(sql, allow_write)

        if validation_error:
            return {"error": validation_error}

        conn = connect_db(self.db_path)

        try:
            return execute_sql(conn, sql)
        finally:
            conn.close()


SQLITE_DB_SYSTEM_MESSAGE = """
You are a SQLite DB agent.

RULES:
- DO NOT explain steps
- DO NOT write "Step 1", "Step 2"
- ONLY output SQL query OR call execute_query
- Example:
  SELECT * FROM customers WHERE Country = 'China' LIMIT 10
"""


_db_agent_cache = {}


def db_agent(name: str, model_client):

    db_path = "/home/priyanshurajchauhan/Desktop/Traning/Week7/src/data/sql/customers.db"

    if db_path in _db_agent_cache:
        return _db_agent_cache[db_path]

    tools_impl = SQLiteDBTools(db_path)

    tools = [
        FunctionTool(
            func=tools_impl.get_db_tables,
            name="get_db_tables",
            description="List all tables in the database"
        ),
        FunctionTool(
            func=tools_impl.inspect_table_schema,
            name="inspect_table_schema",
            description="Get schema of a table"
        ),
        FunctionTool(
            func=tools_impl.execute_query,
            name="execute_query",
            description="Execute SELECT or INSERT SQL query"
        ),
    ]

    agent = AssistantAgent(
        name=name,
        system_message=SQLITE_DB_SYSTEM_MESSAGE,
        model_client=model_client,
        max_tool_iterations=6,
        tools=tools,
    )

    _db_agent_cache[db_path] = agent

    return agent

