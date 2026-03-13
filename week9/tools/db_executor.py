import sqlite3
import re
import os
from typing import Any, Dict, List, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool

# --- Security Patterns ---
FORBIDDEN_SQL_PATTERNS = re.compile(
    r"\b(UPDATE|DELETE|DROP|ALTER|TRUNCATE|ATTACH|DETACH|PRAGMA)\b",
    re.IGNORECASE,
)
ALLOWED_WRITE_PATTERNS = re.compile(
    r"^\s*INSERT\s+INTO\b",
    re.IGNORECASE,
)

# --- Database Utility Functions ---
def connect_db(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)

def list_tables(conn: sqlite3.Connection) -> List[str]:
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return [row[0] for row in cursor.fetchall()]

def get_table_schema(conn: sqlite3.Connection, table_names: List[str]) -> Dict[str, Any]:
    schemas = {}
    for table in table_names:
        cursor = conn.execute(f"PRAGMA table_info({table});")
        schemas[table] = [
            {
                "column": row[1],
                "type": row[2],
                "not_null": bool(row[3]),
                "primary_key": bool(row[5]),
            }
            for row in cursor.fetchall()
        ]
    return schemas

def validate_sql(sql: str, allow_write: bool) -> Optional[str]:
    sql_clean = sql.strip()
    if FORBIDDEN_SQL_PATTERNS.search(sql_clean):
        return "UPDATE / DELETE / DDL statements are forbidden."
    is_insert = bool(ALLOWED_WRITE_PATTERNS.match(sql_clean))
    is_select = sql_clean.lower().startswith("select")
    if is_insert and not allow_write:
        return "INSERT attempted without explicit write permission."
    if not (is_select or is_insert):
        return "Only SELECT and INSERT are allowed."
    if is_select and "limit" not in sql_clean.lower():
        return "SELECT queries must include LIMIT (e.g., LIMIT 10)."
    return None

def execute_sql(conn: sqlite3.Connection, sql: str) -> Dict[str, Any]:
    cursor = conn.execute(sql)
    if cursor.description:
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        return {
            "rows": [dict(zip(columns, row)) for row in rows],
            "row_count": len(rows),
        }
    conn.commit()
    return {"rows_affected": cursor.rowcount}

# --- Tool Implementation Class ---
class SQLiteDBTools:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_db_tables(self) -> dict:
        """List all tables in the SQLite database."""
        conn = connect_db(self.db_path)
        try:
            return {"tables": list_tables(conn)}
        finally:
            conn.close()

    def inspect_table_schema(self, table_name: str) -> dict:
        """Inspect schema of a specific table. Provide the table name as a string."""
        conn = connect_db(self.db_path)
        try:
            return {"schema": get_table_schema(conn, [table_name])}
        finally:
            conn.close()

    def execute_query(self, sql: str, allow_write: bool = False) -> dict:
        """Execute a SELECT or INSERT SQL query. Ensure SELECT queries have a LIMIT."""
        validation_error = validate_sql(sql, allow_write)
        if validation_error:
            return {"error": validation_error}
        conn = connect_db(self.db_path)
        try:
            return execute_sql(conn, sql)
        finally:
            conn.close()

# --- Agent System Message ---
SQLITE_DB_SYSTEM_MESSAGE = """You are a database assistant.
To provide accurate answers, follow this protocol:
1. Use 'get_db_tables' to see existing tables.
2. Use 'inspect_table_schema' for any table you plan to query.
3. Use 'execute_query' with a valid SQL SELECT statement. 
   - ALWAYS include 'LIMIT' in your SELECT queries.
   - Use the exact column names found in the schema.
Summarize the final data for the user clearly."""

# --- Agent Factory Function ---
def db_agent(name: str, model_client) -> AssistantAgent:
    # THE PATH YOU PROVIDED
    db_path = "/home/priyanshurajchauhan/Desktop/Traning/Week7/src/data/sql/customers.db"
    
    tools_impl = SQLiteDBTools(db_path)
    
    # Wrap functions into FunctionTools
    tools = [
        FunctionTool(tools_impl.get_db_tables, name="get_db_tables", description="Lists tables"),
        FunctionTool(tools_impl.inspect_table_schema, name="inspect_table_schema", description="Gets schema for a table"),
        FunctionTool(tools_impl.execute_query, name="execute_query", description="Runs SELECT/INSERT queries"),
    ]
    
    return AssistantAgent(
        name=name,
        system_message=SQLITE_DB_SYSTEM_MESSAGE,
        model_client=model_client,
        max_tool_iterations=8,
        tools=tools,
    )