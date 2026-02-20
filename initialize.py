import sqlite3
from pathlib import Path

filepath = Path.cwd().joinpath("databases", "access_counter.db")
conn = sqlite3.connect()
conn.execute("""
CREATE TABLE IF NOT EXISTS access_counter (
    value INTEGER NOT NULL
)
""")
conn.execute("INSERT OR IGNORE INTO access_counter (rowid, value) VALUES (1, 0)")
conn.commit()
conn.close()
