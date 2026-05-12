from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def detect_intent(message: str) -> str:
    try:
        prompt = f"""
You are an intent classifier.

Classify the user message into exactly one of:
[check_balance, view_transactions, block_card, dispute_transaction, faq_query, talk_to_human]

Examples:
- "what is my balance" → check_balance
- "how much money do i have" → check_balance
- "show my transactions" → view_transactions
- "recent payments" → view_transactions
- "block my card" → block_card
- "i lost my card" → block_card
- "my card is stolen" → block_card
- "freeze my debit card" → block_card
- "talk to human" → talk_to_human

Return ONLY the intent name.

Message: {message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt   # ✅ JUST STRING (this is the fix)
        )

        intent = response.text.strip().lower()
        intent = intent.replace(".", "").replace("\n", "").strip()

        # 🔥 strict validation
        valid_intents = [
            "check_balance",
            "view_transactions",
            "block_card",
            "dispute_transaction",
            "faq_query",
            "talk_to_human"
        ]

        if intent not in valid_intents:
            print("⚠️ Invalid intent from model:", intent)
            return "faq_query"

        return intent

    except Exception as e:
        print("LLM ERROR:", e)

        msg = message.lower()

        if "balance" in msg:
            return "check_balance"
        elif "transaction" in msg:
            return "view_transactions"
        elif "block" in msg or "card" in msg:
            return "block_card"
        elif "human" in msg or "agent" in msg:
            return "talk_to_human"
        else:
            return "faq_query"


if __name__ == "__main__":
    print(detect_intent("how much money do i have"))