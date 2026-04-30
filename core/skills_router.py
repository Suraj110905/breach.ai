# ============================================================
# BREACH — core/skills_router.py
# Routes user input to skills — with permission check
# ============================================================

import importlib
from core.permissions import is_allowed

SKILL_MAP = {
    "open":      "open_app",
    "launch":    "open_app",
    "search":    "web_search",
    "google":    "web_search",
    "look up":   "web_search",
    "time":      "tell_time",
    "date":      "tell_time",
    "what day":  "tell_time",
}


def route(user_input, speak_fn, listen_fn):
    """
    Matches user input to a skill.
    Checks permission before running.
    Returns (response, was_triggered)
    """
    text = user_input.lower()

    for keyword, skill_name in SKILL_MAP.items():
        if keyword in text:

            # ── Permission check ─────────────────────────────
            allowed = is_allowed(skill_name, speak_fn, listen_fn)
            if not allowed:
                return "Permission denied.", True

            # ── Run the skill ────────────────────────────────
            try:
                skill = importlib.import_module(f"skills.{skill_name}")
                response = skill.run(user_input)
                return response, True
            except Exception as e:
                return f"Skill {skill_name} failed: {str(e)}", True

    return None, False