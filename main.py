# ============================================================
# BREACH — Personal AI Assistant
# main.py — Entry point / system boot
# ============================================================

import os
import sys
import time
from dotenv import load_dotenv
from core.voice import speak, listen
from core.brain import think
from core.skills_router import route
from core.state import set_state
from core.wake import wait_for_wake_word
from ui.app import start_ui

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
    print()
    print("  ██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗")
    print("  ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║")
    print("  ██████╔╝██████╔╝█████╗  ███████║██║     ███████║")
    print("  ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║")
    print("  ██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║")
    print("  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝")
    print()
    print("  Personal AI Assistant — Boot Sequence")
    print("  " + "─" * 44)
    print()

    # ── Phase 0: Environment check ───────────────────────────
    log("INFO", "Phase 0 — Checking environment...")
    env_ok = check_environment()

    if not env_ok:
        print()
        log("ERROR", "Boot failed. Fix the issues above and retry.")
        print()
        sys.exit(1)

    # ── Start avatar UI ──────────────────────────────────────
    start_ui()
    time.sleep(1)

    print()
    log("OK",   "All systems nominal")
    log("OK",   "Voice system ready")
    log("OK",   "Avatar UI ready — http://localhost:5000")
    print()
    print("  BREACH is ready.")
    print()

    # ── Conversation loop with wake word ─────────────────────
    set_state("speaking")
    speak("BREACH online. Say Computer to activate me.")
    set_state("idle")

    while True:
        set_state("idle")
        wait_for_wake_word()

        set_state("listening")
        speak("Yes?")
        user_input = listen()

        if not user_input:
            continue

        if any(word in user_input.lower() for word in ["goodbye", "bye", "exit", "quit", "shutdown"]):
            set_state("speaking")
            speak("Shutting down. Goodbye.")
            set_state("idle")
            break

        skill_response, was_triggered = route(user_input, speak, listen)

        if was_triggered:
            set_state("speaking")
            speak(skill_response)
            set_state("idle")
        else:
            set_state("thinking")
            log("INFO", "Thinking...")
            response = think(user_input)
            set_state("speaking")
            speak(response)
            set_state("idle")


if __name__ == "__main__":
    main()