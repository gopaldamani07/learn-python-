import os
import duckdb

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "items.duckdb"
)

con = duckdb.connect(DB_PATH)

con.execute("CREATE SEQUENCE IF NOT EXISTS items_id_seq START 1")
con.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        description VARCHAR,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")


def row_to_dict(r):
    return {"id": r[0], "name": r[1], "description": r[2], "created_at": r[3]}