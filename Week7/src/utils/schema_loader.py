import sqlite3

def load_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    schema = {}
    for (table,) in cursor.fetchall():
        cursor.execute(f"PRAGMA table_info({table});")
        schema[table] = [col[1] for col in cursor.fetchall()]

    conn.close()
    return schema
