
# ============================================================
# BREACH — Personal AI Assistant
# main.py — Entry point / system boot
# ============================================================import os
import sys
from dotenv import load_dotenv

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

    # ── Check Anthropic API key ──────────────────────────────
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        log("ERROR", "ANTHROPIC_API_KEY not found in .env file")
        log("INFO",  "Copy .env.example to .env and add your key")
        log("INFO",  "Get your key: https://console.anthropic.com")
        all_good = False

    elif api_key == "your_anthropic_api_key_here":
        log("WARN",  "ANTHROPIC_API_KEY is still a placeholder — update it")
        all_good = False

    else:
        log("OK", "Anthropic API key loaded")

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
    log("INFO", "Phase 1 (Voice) — coming next")
    print()
    print("  BREACH is ready.")
    print()
    
if __name__ == "__main__":
    main()