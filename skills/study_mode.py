# ============================================================
# BREACH Skill — study_mode
# Quizzes you on any topic using spaced repetition logic
# ============================================================

import json
import os
from datetime import datetime, timedelta

STUDY_FILE = os.path.join("config", "study_data.json")


def load_data():
    if os.path.exists(STUDY_FILE):
        with open(STUDY_FILE, "r") as f:
            return json.load(f)
    return {"topics": {}, "current_topic": None}


def save_data(data):
    with open(STUDY_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Quiz questions per topic ──────────────────────────────────
QUESTIONS = {
    "python": [
        ("What does len() do?",                    "Returns the length of an object"),
        ("What is a list comprehension?",           "A compact way to create lists using a single line"),
        ("What does def keyword do?",               "Defines a function"),
        ("What is the difference between = and ==?","= assigns a value, == compares two values"),
        ("What does import do?",                    "Loads an external module into your script"),
    ],
    "git": [
        ("What does git init do?",                  "Initialises a new Git repository"),
        ("What does git add . do?",                 "Stages all changed files for commit"),
        ("What does git commit do?",                "Saves a snapshot of staged changes"),
        ("What does git push do?",                  "Uploads commits to the remote repository"),
        ("What is a branch?",                       "An independent line of development"),
    ],
    "general": [
        ("What is RAM?",                            "Random Access Memory — temporary fast storage"),
        ("What is an API?",                         "A way for two programs to talk to each other"),
        ("What does CPU stand for?",                "Central Processing Unit"),
        ("What is open source software?",           "Software with publicly available source code"),
    ]
}


def run(user_input):
    data  = load_data()
    text  = user_input.lower()

    # ── Detect topic from speech ──────────────────────────────
    topic = None
    for t in QUESTIONS:
        if t in text:
            topic = t
            break

    if not topic:
        topic = "python"  # default topic

    # ── Pick next question ────────────────────────────────────
    topic_data = data["topics"].get(topic, {"index": 0, "score": 0})
    questions  = QUESTIONS[topic]
    index      = topic_data["index"] % len(questions)
    question, answer = questions[index]

    # Advance index for next time
    topic_data["index"] = index + 1
    data["topics"][topic] = topic_data
    data["current_topic"]  = topic
    save_data(data)

    return (
        f"Study mode activated. Topic: {topic}. "
        f"Question {index + 1} of {len(questions)}: "
        f"{question} "
        f"The answer is: {answer}. "
        f"Say 'next question' to continue."
    )