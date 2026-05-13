from fastapi import FastAPI
from pydantic import BaseModel
from session_store import get_session, save_session
from intent_classifier import detect_intent
from tools import get_balance, get_transactions
from datetime import datetime
from routes.create_user import router as create_user_router
from routes.get_users import router as get_users_router
import requests
import random
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register Routes
app.include_router(create_user_router)
app.include_router(get_users_router)

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

    # 🟠 Cancel
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

        if not session.get("is_authenticated"):

            session["pending_intent"] = "block_card_auth"
            session["current_intent"] = "block_card"

            save_session(req.session_id, session)

            return {
                "reply": "Please enter your 8 digit account number to continue.",
                "session": session
            }

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

        # user typed another request
        if not msg.isdigit():

            session["pending_intent"] = None
            session["current_intent"] = None

            save_session(req.session_id, session)

            return chat(ChatRequest(
                message=msg,
                session_id=req.session_id
            ))

        # validate account number
        if len(msg) != 8:

            reply = "Invalid account number. Please try again."

        else:

            session["data"]["account_number"] = msg

            session["pending_intent"] = "awaiting_otp"

            otp = str(random.randint(100000, 999999))

            session["data"]["otp"] = otp

            session["data"]["otp_created_at"] = datetime.now().isoformat()

            print("DEBUG OTP:", otp)

            reply = "6 digit OTP sent to your registered mobile number."

        save_session(req.session_id, session)

        return {
            "reply": reply,
            "session": session
        }

    # 🔵 OTP FLOW
    if session["pending_intent"] == "awaiting_otp":

        otp_time = session["data"].get("otp_created_at")

        # missing timestamp
        if not otp_time:

            session["pending_intent"] = None

            save_session(req.session_id, session)

            return {
                "reply": "OTP expired. Please request a new OTP.",
                "session": session
            }

        # convert string → datetime
        otp_time = datetime.fromisoformat(otp_time)

        # expiry check
        if (datetime.now() - otp_time).total_seconds() > 60:

            session["pending_intent"] = None

            session["data"].pop("otp", None)
            session["data"].pop("otp_created_at", None)

            save_session(req.session_id, session)

            return {
                "reply": "OTP expired. Please start again.",
                "session": session
            }

        # validate OTP
        if msg != session["data"].get("otp"):

            reply = "Invalid OTP. Please try again."

        else:

            session["is_authenticated"] = True

            # DEMO ONLY
            session["user_id"] = "user_123"

            # session login timestamp
            session["data"]["authenticated_at"] = datetime.now().isoformat()

            # clear OTP after use
            session["data"].pop("otp", None)
            session["data"].pop("otp_created_at", None)

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

    # 🟢 Intent Detection
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

    # 🟡 Block Card
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

    # 🟡 Human
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