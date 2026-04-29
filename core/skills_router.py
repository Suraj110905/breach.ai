# ============================================================
# BREACH — core/skills_router.py
# Reads user input and routes to the correct skill
# ============================================================

import importlib
import os


# ── Skill keyword map ────────────────────────────────────────
# Each entry: "keyword in speech" → "skill filename in /skills"
SKILL_MAP = {
    "open":        "open_app",
    "launch":      "open_app",
    "search":      "web_search",
    "google":      "web_search",
    "look up":     "web_search",
    "time":        "tell_time",
    "date":        "tell_time",
    "what day":    "tell_time",
}


def route(user_input):
    """
    Checks user_input against SKILL_MAP keywords.
    If a match is found, loads and runs that skill.
    Returns (skill_response, skill_was_triggered)
    """
    text = user_input.lower()

    for keyword, skill_name in SKILL_MAP.items():
        if keyword in text:
            try:
                # Dynamically load the skill module from /skills folder
                skill = importlib.import_module(f"skills.{skill_name}")
                response = skill.run(user_input)
                return response, True
            except Exception as e:
                return f"Skill {skill_name} failed: {str(e)}", True

    # No skill matched — let Gemini handle it
    return None, False