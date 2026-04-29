# BREACH Skill — tell_time
# Tells the current time and date

from datetime import datetime


def run(user_input):
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")       # e.g. 03:45 PM
    date_str = now.strftime("%A, %d %B %Y")   # e.g. Thursday, 30 April 2026
    return f"It is {time_str} on {date_str}."