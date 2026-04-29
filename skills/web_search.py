# BREACH Skill — web_search
# Opens a Google search in the default browser

import webbrowser
import urllib.parse


def run(user_input):
    # Strip trigger words to get the actual search query
    query = user_input.lower()
    for word in ["search", "google", "look up", "find", "breach"]:
        query = query.replace(word, "")
    query = query.strip()

    if not query:
        return "What would you like me to search for?"

    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return f"Searching Google for: {query}" 