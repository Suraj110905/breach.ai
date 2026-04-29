# BREACH - Personal AI Assistant

BREACH is a voice-activated personal AI assistant with a modular skill system,
long-term memory, permission-based system access, and an animated avatar UI.

## Stack
- Python 3.10+
- Claude API (Anthropic)
- faster-whisper (speech-to-text)
- pyttsx3 (text-to-speech)
- ChromaDB (long-term memory)
- Electron / Three.js (avatar UI)

## Setup
1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your API keys
4. Run `python main.py`

## Architecture
See docs/architecture.md (coming soon)