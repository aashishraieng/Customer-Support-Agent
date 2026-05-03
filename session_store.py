import json
from database import conn, cursor

def get_session(session_id):
    cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()

    if row:
        return {
            "is_authenticated": bool(row[1]),
            "user_id": row[2],
            "data": json.loads(row[3]) if row[3] else {},
            "pending_intent": row[4],
            "current_intent": row[5]
        }

    # create new session
    session = {
        "is_authenticated": False,
        "user_id": None,
        "data": {},
        "pending_intent": None,
        "current_intent": None
    }

    save_session(session_id, session)
    return session


def save_session(session_id, session):
    cursor.execute("""
    INSERT OR REPLACE INTO sessions 
    (session_id, is_authenticated, user_id, data, pending_intent, current_intent)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        int(session["is_authenticated"]),
        session["user_id"],
        json.dumps(session["data"]),
        session["pending_intent"],
        session["current_intent"]
    ))

    conn.commit()