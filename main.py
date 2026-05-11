
# ============================================================
# BREACH — Personal AI Assistant
# main.py — Entry point / system boot
# ============================================================import os
import os
import sys
from dotenv import load_dotenv
from core.voice import speak, listen
from core.brain import think
from core.skills_router import route
import time
from dotenv import load_dotenv
from core.voice import speak, listen
from core.brain import think
from core.skills_router import route
from core.state import set_state
from ui.app import start_ui
from core.wake import wait_for_wake_word

load_dotenv()

def log(status, message):
    symbols = {
        "OK":    "✓",
        "WARN":  "!",
        "ERROR": "✗",
        "INFO":  "→"
    }
    symbol = symbols.get(status, "?")
    print(f"  [{symbol}] {message}")

def check_environment():
    """
    Verifies all required environment variables exist.
    Returns True if everything is fine, False if something is missing.
    """
    all_good = True

    # ── Check Gemini API key ──────────────────────────────────
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        log("ERROR", "GEMINI_API_KEY not found in .env file")
        log("INFO",  "Get your key: https://aistudio.google.com")
        all_good = False

    elif api_key == "your_gemini_api_key_here":
        log("WARN",  "GEMINI_API_KEY is still a placeholder — update it")
        all_good = False

    else:
        log("OK", "Gemini API key loaded")

    # ── Check Picovoice key (optional) ───────────────────────
    pv_key = os.getenv("PICOVOICE_KEY")

    if not pv_key or pv_key == "your_picovoice_key_here":
        log("WARN", "PICOVOICE_KEY not set — wake word disabled, using direct listen mode")
    else:
        log("OK", "Picovoice wake word key loaded")

    return all_good

def main():
    # ── Start avatar UI ──────────────────────────────────────
    start_ui()
    time.sleep(1)  # give Flask a moment to start

    # ── Boot confirmed ───────────────────────────────────────
    print()
    log("OK",   "All systems nominal")
    log("OK",   "Voice system ready")
    log("OK",   "Avatar UI ready")
    print()
    print("  BREACH is ready.")
    print()

    set_state("speaking")
    speak("BREACH online. How can I help you?")
    set_state("idle")

    # ── Conversation loop with wake word ─────────────────────
    set_state("speaking")
    speak("BREACH online. Say Computer to activate me.")
    set_state("idle")

    while True:
        # ── Wait for wake word ────────────────────────────────
        set_state("idle")
        wait_for_wake_word()

        # ── Wake word heard — now listen for command ──────────
        set_state("listening")
        speak("Yes?")
        user_input = listen()

        if not user_input:
            continue

        # ── Exit commands ─────────────────────────────────────
        if any(word in user_input.lower() for word in ["goodbye", "bye", "exit", "quit", "shutdown"]):
            set_state("speaking")
            speak("Shutting down. Goodbye.")
            set_state("idle")
            break

        # ── Try skills first ──────────────────────────────────
        skill_response, was_triggered = route(user_input, speak, listen)

        if was_triggered:
            set_state("speaking")
            speak(skill_response)
            set_state("idle")
        else:
            # ── Send to Gemini brain ──────────────────────────
            set_state("thinking")
            log("INFO", "Thinking...")
            response = think(user_input)
            set_state("speaking")
            speak(response)
            set_state("idle")
    
if __name__ == "__main__":
    main()