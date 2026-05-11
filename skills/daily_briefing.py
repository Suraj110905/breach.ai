# ============================================================
# BREACH Skill — daily_briefing
# Gives a morning briefing: time, date, weather, motivation
# ============================================================

import requests
from datetime import datetime


# ── Motivational lines BREACH cycles through ─────────────────
MOTIVATIONS = [
    "Every expert was once a beginner. Keep building.",
    "The best time to start was yesterday. The next best time is now.",
    "Small steps every day compound into massive results.",
    "You don't rise to the level of your goals. You fall to the level of your systems.",
    "Code it. Break it. Fix it. Repeat.",
    "The only way to do great work is to love what you do.",
    "Push yourself because no one else is going to do it for you.",
]


def get_weather(city="Bhopal"):
    """
    Fetches current weather using Open-Meteo (free, no API key needed).
    Defaults to Bhopal — change city name to update coordinates.
    """
    # Bhopal coordinates
    lat, lon = 23.2599, 77.4126

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,weathercode"
            f"&timezone=Asia/Kolkata"
        )
        res  = requests.get(url, timeout=5)
        data = res.json()

        temp = data["current"]["temperature_2m"]
        code = data["current"]["weathercode"]

        # Simplified weather code mapping
        if code == 0:
            condition = "clear skies"
        elif code in [1, 2, 3]:
            condition = "partly cloudy"
        elif code in [51, 53, 55, 61, 63, 65]:
            condition = "rainy"
        elif code in [71, 73, 75]:
            condition = "snowy"
        elif code in [95, 96, 99]:
            condition = "stormy"
        else:
            condition = "mixed conditions"

        return f"{temp}°C with {condition}"

    except Exception:
        return "weather unavailable right now"


def run(user_input):
    now        = datetime.now()
    time_str   = now.strftime("%I:%M %p")
    date_str   = now.strftime("%A, %d %B %Y")
    weather    = get_weather()

    # Pick motivation based on day of week so it changes daily
    motivation = MOTIVATIONS[now.weekday() % len(MOTIVATIONS)]

    briefing = (
        f"Good morning. "
        f"It is {time_str} on {date_str}. "
        f"Weather in Bhopal is {weather}. "
        f"Here is your thought for today — {motivation}"
    )

    return briefing