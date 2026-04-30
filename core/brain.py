# ============================================================
# BREACH — core/brain.py
# Thinking engine with long-term memory injection
# ============================================================

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from core.memory import recall_relevant, save_conversation, get_all_preferences

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are BREACH, a personal AI assistant running locally on the user's computer.
You are sharp, efficient, and direct. You never waste words.
You help with daily tasks, answer questions, and learn the user's preferences over time.
Keep responses short and conversational — this is a voice assistant, not an essay writer.
Maximum 2-3 sentences unless the user asks for detail.
If you learn something personal about the user (name, preferences, habits), remember it.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

chat_session = model.start_chat(history=[])


def think(user_input):
    """
    Sends user input to Gemini with relevant memory injected.
    Saves the exchange to long-term memory after every response.
    """
    try:
        # ── Inject relevant memories into prompt ─────────────
        memory_context = recall_relevant(user_input)
        preferences    = get_all_preferences()

        # Build full prompt with memory context
        if memory_context or preferences:
            full_prompt = ""
            if preferences:
                full_prompt += f"What you know about the user:\n{preferences}\n\n"
            if memory_context:
                full_prompt += f"{memory_context}\n\n"
            full_prompt += f"User just said: {user_input}"
        else:
            full_prompt = user_input

        time.sleep(2)
        response = chat_session.send_message(full_prompt)
        reply    = response.text.strip()

        # ── Save this exchange to memory ──────────────────────
        save_conversation(user_input, reply)

        return reply

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return "Hit my rate limit — please wait a few seconds and try again."
        return f"I encountered an error: {error_msg}"