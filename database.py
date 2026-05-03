import sqlite3

conn = sqlite3.connect("bank.db", check_same_thread=False)
cursor = conn.cursor()

# Create session table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    is_authenticated INTEGER,
    user_id TEXT,
    data TEXT,
    pending_intent TEXT,
    current_intent TEXT
)
""")

conn.commit()