import sqlite3
import pandas as pd

CSV_PATH = "src/data/raw/customers-1000.csv"
DB_PATH = "src/data/sql/customers.db"
TABLE_NAME = "customers"

def csv_to_sqlite():
    df = pd.read_csv(CSV_PATH)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Loaded {len(df)} rows into '{TABLE_NAME}' table")

if __name__ == "__main__":
    csv_to_sqlite()
