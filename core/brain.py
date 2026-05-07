# ============================================================
# BREACH — core/brain.py
# Thinking engine using new google-genai SDK
# ============================================================

import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
from core.memory import recall_relevant, save_conversation, get_all_preferences

load_dotenv()

# ── Setup client ─────────────────────────────────────────────
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ── Model to use ─────────────────────────────────────────────
MODEL = "gemini-2.0-flash"   # we will update this after seeing your model list

# ── System prompt ────────────────────────────────────────────
SYSTEM_PROMPT = """
You are BREACH, a personal AI assistant running locally on the user's computer.
You are sharp, efficient, and direct. You never waste words.
Keep responses short and conversational — this is a voice assistant, not an essay writer.
Maximum 2-3 sentences unless the user asks for detail.
"""

# ── Conversation history (short term memory) ─────────────────
history = []


def think(user_input):
    """
    Sends user input to Gemini and returns response.
    Injects long term memory into every prompt.
    Retries automatically on rate limit.
    """
    global history

    # ── Build prompt with memory context ─────────────────────
    memory_context = recall_relevant(user_input)
    preferences    = get_all_preferences()

    full_prompt = ""
    if preferences:
        full_prompt += f"What you know about the user:\n{preferences}\n\n"
    if memory_context:
        full_prompt += f"{memory_context}\n\n"
    full_prompt += f"User: {user_input}"

    # ── Add to history ────────────────────────────────────────
    history.append({"role": "user", "parts": [{"text": full_prompt}]})

    max_retries = 3

    for attempt in range(max_retries):
        try:
            time.sleep(3)

            response = client.models.generate_content(
                model=MODEL,
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=200,
                    temperature=0.7,
                )
            )

            reply = response.text.strip()

            # Save assistant reply to history
            history.append({"role": "model", "parts": [{"text": reply}]})

            # Keep history from growing too large (last 10 exchanges)
            if len(history) > 20:
                history = history[-20:]

            # Save to long term memory
            save_conversation(user_input, reply)

            return reply

        except Exception as e:
            error_msg = str(e)

            if "429" in error_msg or "quota" in error_msg.lower():
                wait = (attempt + 1) * 10
                print(f"  [!] Rate limit — waiting {wait}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                continue

            return f"Error: {error_msg}"

    return "Still rate limited. Please wait a minute and try again."


if __name__ == "__main__":
    print("Testing brain...")
    reply = think("Hello, introduce yourself in one sentence.")
    print(f"BREACH: {reply}")