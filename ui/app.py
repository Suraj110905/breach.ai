
# ============================================================
# BREACH — ui/app.py
# Local Flask server that powers the avatar UI
# ============================================================

from flask import Flask, render_template, jsonify, request
import threading

app = Flask(__name__)

# ── BREACH state ─────────────────────────────────────────────
# idle | listening | thinking | speaking
current_state = {"state": "idle"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(current_state)


@app.route("/state", methods=["POST"])
def set_state():
    data = request.get_json()
    current_state["state"] = data.get("state", "idle")
    return jsonify({"ok": True})


def start_ui():
    """Starts Flask in a background thread so it doesn't block BREACH."""
    thread = threading.Thread(
        target=lambda: app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    thread.start()
    print("  [✓] Avatar UI running at http://localhost:5000")