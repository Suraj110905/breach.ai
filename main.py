
# ============================================================
# BREACH — Personal AI Assistant
# main.py — Entry point / system boot
# ============================================================import os
import sys
from dotenv import load_dotenv
from core.voice import speak, listen
from core.brain import think

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

    return all_good

def main():
    # ── Boot header ─────────────────────────────────────────
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

    # ── All systems go ───────────────────────────────────────
    print()
    log("OK",   "All systems nominal")
    log("OK",   "Voice system ready")
    print()
    print("  BREACH is ready.")
    print()
    speak("BREACH online. How can I help you?")
    # ── Conversation loop ────────────────────────────────────
    speak("BREACH online. How can I help you?")

    while True:
        user_input = listen()

        if not user_input:
            continue   # heard nothing, listen again

        # Exit commands
        if any(word in user_input.lower() for word in ["goodbye", "bye", "exit", "quit", "shutdown"]):
            speak("Shutting down. Goodbye.")
            break

        # Think and respond
        log("INFO", "Thinking...")
        response = think(user_input)
        speak(response)
    
if __name__ == "__main__":
    main()