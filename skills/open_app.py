# BREACH Skill — open_app
# Opens applications on Windows by name

import subprocess
import os


# Map spoken app names to their executable or command
APP_MAP = {
    "chrome":     "chrome",
    "notepad":    "notepad",
    "calculator": "calc",
    "explorer":   "explorer",
    "spotify":    "spotify",
    "vs code":    "code",
    "vscode":     "code",
    "terminal":   "cmd",
}


def run(user_input):
    text = user_input.lower()

    for app_name, command in APP_MAP.items():
        if app_name in text:
            try:
                subprocess.Popen(command, shell=True)
                return f"Opening {app_name}."
            except Exception as e:
                return f"Could not open {app_name}: {str(e)}"

    return "I'm not sure which app to open. Try saying the app name clearly."