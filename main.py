from fastapi import FastAPI
from pydantic import BaseModel
from session_store import get_session, save_session
from intent_classifier import detect_intent
from tools import get_balance, get_transactions
from datetime import datetime
import requests

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
def chat(req: ChatRequest):

    session = get_session(req.session_id)
    msg = req.message.lower().strip()

    # 🔴 Logout
    if msg == "logout":

        session.update({
            "is_authenticated": False,
            "user_id": None,
            "data": {},
            "pending_intent": None,
            "current_intent": None
        })

        save_session(req.session_id, session)

        return {
            "reply": "You have been logged out.",
            "session": session
        }

    # 🟠 Cancel current flow
    if msg == "cancel":

        session.update({
            "pending_intent": None,
            "current_intent": None,
            "data": {}
        })

        save_session(req.session_id, session)

        return {
            "reply": "Request cancelled. How can I help you?",
            "session": session
        }

    # 🔵 BLOCK CARD FLOW
    if session["pending_intent"] == "block_card":

        # enforce auth
        if not session.get("is_authenticated"):

            session["pending_intent"] = "block_card_auth"
            session["current_intent"] = "block_card"

            save_session(req.session_id, session)

            return {
                "reply": "Please enter your 8 Digit account number to continue.",
                "session": session
            }

        # validate last 4 digits
        if not msg.isdigit() or len(msg) != 4:

            reply = "Invalid input. Please enter last 4 digits of your card."

        else:

            session["data"]["card_last4"] = msg

            try:
                res = requests.post(
                    "http://localhost:5678/webhook/block-card",
                    json={
                        "user_id": session.get("user_id"),
                        "card_last4": msg
                    }
                )

                print("n8n status:", res.status_code)

            except Exception as e:
                print("n8n error:", e)

            reply = "Your request has been submitted. Connecting you to a support agent..."

            session["pending_intent"] = None
            session["current_intent"] = None

        save_session(req.session_id, session)

        return {
            "reply": reply,
            "session": session
        }

    # 🔵 ACCOUNT NUMBER FLOW
    if session["pending_intent"] in [
        "check_balance",
        "view_transactions",
        "block_card_auth"
    ]:

        # user typed another natural-language query
        if not msg.isdigit():

            session["pending_intent"] = None
            session["current_intent"] = None

            save_session(req.session_id, session)

            return chat(ChatRequest(
                message=msg,
                session_id=req.session_id
            ))

        # strict account number validation
        if len(msg) != 8:

            reply = "Invalid account number. Please try again."

        else:

            session["data"]["account_number"] = msg
            session["pending_intent"] = "awaiting_otp"

            reply = "6 digit OTP sent to your registered mobile number."

        save_session(req.session_id, session)

        return {
            "reply": reply,
            "session": session
        }

    # 🔵 OTP FLOW
    if session["pending_intent"] == "awaiting_otp":

        if msg != "123456":

            reply = "Invalid OTP. Please try again."

        else:

            session["is_authenticated"] = True

            # ⚠️ DEMO ONLY
            session["user_id"] = "user_123"

            # ✅ session timeout timestamp
            session["data"]["authenticated_at"] = datetime.now().isoformat()

            # continue original intent
            if session.get("current_intent") == "check_balance":

                balance = get_balance(session["user_id"])

                reply = f"Your current balance is ₹{balance}"

                session["pending_intent"] = None
                session["current_intent"] = None

            elif session.get("current_intent") == "view_transactions":

                txns = get_transactions(session["user_id"])

                reply = "Last 5 transactions:\n" + "\n".join(txns)

                session["pending_intent"] = None
                session["current_intent"] = None

            elif session.get("current_intent") == "block_card":

                session["pending_intent"] = "block_card"

                reply = "Please enter last 4 digits of your card."

        save_session(req.session_id, session)

        return {
            "reply": reply,
            "session": session
        }

    # 🟢 Greeting
    if msg in ["hi", "hello"]:

        return {
            "reply": "Welcome to Bank Support. How can I help you?",
            "session": session
        }

    # 🟢 AI Intent Detection
    intent = detect_intent(msg)

    print("INTENT:", intent)

    # 🟡 Balance
    if intent == "check_balance":

        if session["is_authenticated"]:

            balance = get_balance(session["user_id"])

            reply = f"Your current balance is ₹{balance}"

        else:

            session["pending_intent"] = "check_balance"
            session["current_intent"] = "check_balance"

            reply = "Please enter your account number."

    # 🟡 Transactions
    elif intent == "view_transactions":

        if session["is_authenticated"]:

            txns = get_transactions(session["user_id"])

            reply = "Last 5 transactions:\n" + "\n".join(txns)

        else:

            session["pending_intent"] = "view_transactions"
            session["current_intent"] = "view_transactions"

            reply = "Please enter your account number."

    # 🟡 Block card
    elif intent == "block_card":

        if not session["is_authenticated"]:

            session["pending_intent"] = "block_card_auth"
            session["current_intent"] = "block_card"

            reply = "Please enter your account number to continue."

        else:

            session["pending_intent"] = "block_card"
            session["current_intent"] = "block_card"

            reply = "Please enter last 4 digits of your card."

    # 🟡 FAQ
    elif intent == "faq_query":

        reply = "This is a general banking query."

    # 🟡 Human handoff
    elif intent == "talk_to_human":

        reply = "Connecting you to a support agent..."

    # ⚫ fallback
    else:

        reply = "I didn't understand. Please try again."

    save_session(req.session_id, session)

    return {
        "reply": reply,
        "session": session
    }