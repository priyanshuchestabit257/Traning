import sqlite3


class LongTermMemory:

    def __init__(self, db_path="memory/long_term.db"):

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
        """)

        self.conn.commit()

    def store(self, content):

        self.cursor.execute(
            "INSERT INTO memory (content) VALUES (?)",
            (content,)
        )

        self.conn.commit()

    def fetch_all(self):

        self.cursor.execute("SELECT content FROM memory")

        return [row[0] for row in self.cursor.fetchall()]