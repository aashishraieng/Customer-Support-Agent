from fastapi import FastAPI
from pydantic import BaseModel
from session_store import get_session
from intent_classifier import detect_intent
from tools import get_balance, get_transactions
from session_store import get_session, save_session
app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
def chat(req: ChatRequest):
    session = get_session(req.session_id)

    msg = req.message.lower().strip()

    # 🔴 1. Logout
    if msg == "logout":
        session["is_authenticated"] = False
        session["user_id"] = None
        session["data"] = {}
        session["pending_intent"] = None
        session["current_intent"] = None

        return {
            "reply": "You have been logged out.",
            "session": session
        }

    # 🟠 Cancel
    if msg == "cancel":
        session["pending_intent"] = None
        session["current_intent"] = None
        session["data"] = {}

        return {
            "reply": "Request cancelled. How can I help you?",
            "session": session
        }

    # 🔵 2. Ongoing flow FIRST

    if session["pending_intent"] in ["check_balance", "view_transactions"]:
        if not msg.isdigit() or len(msg) < 6:
            reply = "Invalid account number. Please try again."
        else:
            session["data"]["account_number"] = msg
            session["pending_intent"] = "awaiting_otp"
            reply = "OTP sent to your registered mobile number."

        save_session(req.session_id, session)
        return {"reply": reply, "session": session}

    if session["pending_intent"] == "awaiting_otp":
        if msg != "123456":
            reply = "Invalid OTP. Please try again."
        else:
            session["is_authenticated"] = True
            session["user_id"] = "user_123"

            if session.get("current_intent") == "check_balance":
                balance = get_balance(session.get("user_id"))
                reply = f"Your current balance is ₹{balance}"

            elif session.get("current_intent") == "view_transactions":
                txns = get_transactions(session.get("user_id"))
                reply = "Last 5 transactions:\n" + "\n".join(txns)

            session["pending_intent"] = None
            session["current_intent"] = None

        save_session(req.session_id, session)
        return {"reply": reply, "session": session}

    # 🟢 3. AI Intent Detection (NEW)

    intent = detect_intent(msg)

    # Greeting (keep rule-based, faster + cheaper)
    if msg in ["hi", "hello"]:
        reply = "Welcome to Bank Support. How can I help you?"

    elif intent == "check_balance":
        if session["is_authenticated"]:
            balance = get_balance(session.get("user_id"))
            reply = f"Your current balance is ₹{balance}"
        else:
            session["pending_intent"] = "check_balance"
            session["current_intent"] = "check_balance"
            reply = "Please enter your account number."

    elif intent == "view_transactions":
        if session["is_authenticated"]:
            txns = get_transactions(session.get("user_id"))
            reply = "Last 5 transactions:\n" + "\n".join(txns)
        else:
            session["pending_intent"] = "view_transactions"
            session["current_intent"] = "view_transactions"
            reply = "Please enter your account number."

    elif intent == "faq_query":
        reply = "This is a general banking query. (FAQ system coming next)"

    elif intent == "talk_to_human":
        reply = "Connecting you to a support agent..."

    else:
        reply = "I didn't understand. Please try again."

    save_session(req.session_id, session)
    return {
        "reply": reply,
        "session": session
    }