# ============================================================
# BREACH — core/brain.py
# The thinking engine — sends text to Gemini, returns response
# ============================================================

import os
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
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

# ── Conversation history (short-term memory) ─────────────────
# Stores the current session's back-and-forth
chat_session = model.start_chat(history=[])


def think(user_input):
    """
    Sends user_input to Gemini and returns BREACH's response text.
    Maintains conversation history automatically within the session.
    """
    try:
        response = chat_session.send_message(user_input)
        return response.text.strip()

    except Exception as e:
        return f"I encountered an error: {str(e)}"


if __name__ == "__main__":
    # Quick test — ask BREACH something
    print("Testing brain connection...")
    reply = think("Hello BREACH, introduce yourself in one sentence.")
    print(f"BREACH: {reply}")

    # Test memory — does it remember context?
    reply2 = think("What did I just ask you?")
    print(f"BREACH: {reply2}")