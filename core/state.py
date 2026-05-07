# ============================================================
# BREACH — core/state.py
# Updates the avatar UI state from anywhere in the codebase
# ============================================================

import requests

UI_URL = "http://localhost:5000/state"


def set_state(state):
    """
    Sets BREACH avatar state.
    state: "idle" | "listening" | "thinking" | "speaking"
    """
    try:
        requests.post(UI_URL, json={"state": state}, timeout=0.5)
    except Exception:
        pass  # UI not running — silently skip, never crash core