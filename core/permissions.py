# ============================================================
# BREACH — core/permissions.py
# Permission gate — every skill passes through here first
# ============================================================

import yaml
import os

CONFIG_PATH = os.path.join("config", "permissions.yaml")


def load_permissions():
    """Reads permissions.yaml and returns the skills dict."""
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    return config.get("skills", {})


def is_allowed(skill_name, speak_fn, listen_fn):
    """
    Checks if a skill is permitted to run.

    Returns True if allowed, False if denied or user said no.

    speak_fn and listen_fn are passed in so the permission
    system can talk to the user without importing voice directly
    (avoids circular imports).
    """
    permissions = load_permissions()

    # Default to ask if skill not listed
    level = permissions.get(skill_name, "ask")

    if level == "allow":
        return True

    elif level == "deny":
        speak_fn(f"I'm not allowed to run {skill_name}. It's blocked in your permissions config.")
        return False

    elif level == "ask":
        speak_fn(f"I need permission to run {skill_name}. Say yes to allow or no to block.")
        response = listen_fn()
        if response and any(word in response.lower() for word in ["yes", "yeah", "sure", "allow", "ok", "okay"]):
            return True
        else:
            speak_fn("Okay, I won't do that.")
            return False

    return False