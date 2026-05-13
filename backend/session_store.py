sessions = {}


def get_session(session_id):

    if session_id not in sessions:

        sessions[session_id] = {
            "is_authenticated": False,
            "user_id": None,
            "data": {},
            "pending_intent": None,
            "current_intent": None
        }

    return sessions[session_id]


def save_session(session_id, session_data):

    sessions[session_id] = session_data