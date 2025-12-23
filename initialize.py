import sqlite3
conn = sqlite3.connect("main.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS access_counter (
    value INTEGER NOT NULL
)
""")
conn.execute("INSERT OR IGNORE INTO access_counter (rowid, value) VALUES (1, 0)")
conn.commit()
conn.close()
