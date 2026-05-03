from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def detect_intent(message: str) -> str:
    try:
        prompt = f"""
You are an intent classifier.

Classify the user message into exactly one of:
[check_balance, view_transactions, block_card, dispute_transaction, faq_query, talk_to_human]

Return ONLY the intent name.

Message: {message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt   # ✅ JUST STRING (this is the fix)
        )

        return response.text.strip().lower()

    except Exception as e:
        print("LLM ERROR:", e)

        msg = message.lower()

        if "balance" in msg:
            return "check_balance"
        elif "transaction" in msg:
            return "view_transactions"
        elif "human" in msg or "agent" in msg:
            return "talk_to_human"
        else:
            return "faq_query"


if __name__ == "__main__":
    print(detect_intent("how much money do i have"))