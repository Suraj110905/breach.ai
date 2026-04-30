# ============================================================
# BREACH — core/memory.py
# Long-term memory using ChromaDB (local vector database)
# ============================================================

import os
import chromadb
from datetime import datetime

# ── Setup ChromaDB local storage ────────────────────────────
# All memory is stored in /chroma_db folder inside your project
# This folder is in .gitignore — your personal data never gets pushed
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)

# ── Two memory collections ───────────────────────────────────
# conversations → stores every exchange between you and BREACH
# preferences  → stores facts BREACH learns about you
conversations = client.get_or_create_collection("conversations")
preferences   = client.get_or_create_collection("preferences")


def save_conversation(user_input, breach_response):
    """
    Saves one exchange (what you said + what BREACH said) to memory.
    Each entry gets a unique ID based on timestamp.
    """
    timestamp = datetime.now().isoformat()
    entry_id  = f"conv_{timestamp}"

    conversations.add(
        documents=[f"User: {user_input}\nBREACH: {breach_response}"],
        metadatas=[{"timestamp": timestamp, "type": "conversation"}],
        ids=[entry_id]
    )


def save_preference(key, value):
    """
    Saves a personal fact about the user.
    Example: save_preference("name", "Suraj")
    Example: save_preference("favourite language", "Python")
    Uses key as ID so updating the same key overwrites old value.
    """
    preferences.upsert(
        documents=[f"{key}: {value}"],
        metadatas=[{"key": key, "updated": datetime.now().isoformat()}],
        ids=[f"pref_{key}"]
    )


def recall_relevant(query, n=3):
    """
    Searches memory for entries most relevant to the current query.
    Returns a summary string to inject into BREACH's context.
    n = how many past memories to retrieve
    """
    results = []

    # Search conversations
    try:
        conv_results = conversations.query(
            query_texts=[query],
            n_results=min(n, conversations.count())
        )
        if conv_results["documents"][0]:
            results.extend(conv_results["documents"][0])
    except Exception:
        pass

    # Search preferences
    try:
        pref_results = preferences.query(
            query_texts=[query],
            n_results=min(n, preferences.count())
        )
        if pref_results["documents"][0]:
            results.extend(pref_results["documents"][0])
    except Exception:
        pass

    if not results:
        return ""

    # Format as a clean context block for Gemini
    memory_block = "Relevant memory:\n" + "\n".join(f"- {r}" for r in results)
    return memory_block


def get_all_preferences():
    """Returns all stored user preferences as a formatted string."""
    try:
        if preferences.count() == 0:
            return ""
        all_prefs = preferences.get()
        return "\n".join(f"- {doc}" for doc in all_prefs["documents"])
    except Exception:
        return ""