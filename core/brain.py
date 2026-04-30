# ============================================================
# BREACH — core/brain.py
# The thinking engine — sends text to Gemini, returns response
# ============================================================

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ── Configure Gemini ─────────────────────────────────────────
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ── System prompt — defines who BREACH is ───────────────────
SYSTEM_PROMPT = """
You are BREACH, a personal AI assistant running locally on the user's computer.
You are sharp, efficient, and direct. You never waste words.
You help with daily tasks, answer questions, and learn the user's preferences over time.
Keep responses short and conversational — this is a voice assistant, not an essay writer.
Maximum 2-3 sentences unless the user asks for detail.
"""

# ── Load model ───────────────────────────────────────────────
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

# ── Conversation history (short-term memory) ─────────────────
chat_session = model.start_chat(history=[])


def think(user_input):
    """
    Sends user_input to Gemini and returns BREACH's response text.
    Maintains conversation history automatically within the session.
    """
    try:
        time.sleep(2)  # small buffer to avoid free tier rate limit
        response = chat_session.send_message(user_input)
        return response.text.strip()

    except Exception as e:
        error_msg = str(e)

        # Rate limit hit — give a clean message instead of raw error
        if "429" in error_msg or "quota" in error_msg.lower():
            return "I need a moment. Hit my rate limit — please wait a few seconds and try again."

        return f"I encountered an error: {error_msg}"


if __name__ == "__main__":
    print("Testing brain connection...")
    reply = think("Hello BREACH, introduce yourself in one sentence.")
    print(f"BREACH: {reply}")

    reply2 = think("What did I just ask you?")
    print(f"BREACH: {reply2}")