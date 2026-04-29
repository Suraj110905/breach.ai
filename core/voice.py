# ============================================================
# BREACH — core/voice.py
# Handles all voice input (mic → text) and output (text → speech)
# ============================================================

import sys
import numpy as np
import sounddevice as sd
import pyttsx3
from faster_whisper import WhisperModel

# ── Constants ────────────────────────────────────────────────
SAMPLE_RATE    = 16000   # Whisper expects 16kHz audio
RECORD_SECONDS = 5       # How long BREACH listens per cycle
CHANNELS       = 1       # Mono audio

# ── Load Whisper model once at import time ───────────────────
# "base" is fast and accurate enough for commands
# first run downloads ~150MB model file automatically
print("  [→] Loading Whisper model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
print("  [✓] Whisper model ready")

# ── Load TTS engine once at import time ─────────────────────
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 175)    # speaking speed (words/min)
tts_engine.setProperty("volume", 1.0)  # volume 0.0 to 1.0


def speak(text):
    """
    BREACH speaks a given text string out loud.
    """
    print(f"  [BREACH] {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()


def listen():
    """
    Records audio from the microphone for RECORD_SECONDS duration.
    Returns the transcribed text string, or empty string if nothing heard.
    """
    print(f"  [→] Listening for {RECORD_SECONDS} seconds...")

    # Record raw audio from mic
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )
    sd.wait()  # Block until recording is done

    # Flatten to 1D array (Whisper needs this shape)
    audio_flat = audio.flatten()

    # Transcribe using Whisper
    segments, _ = whisper_model.transcribe(audio_flat, language="en")

    # Join all spoken segments into one string
    text = " ".join([seg.text for seg in segments]).strip()

    if text:
        print(f"  [✓] You said: {text}")
    else:
        print("  [!] Nothing heard")

    return text


if __name__ == "__main__":
    # Quick test: BREACH speaks, then listens, then repeats what it heard
    speak("Hello. I am BREACH. Say something and I will repeat it back.")
    heard = listen()
    if heard:
        speak(f"You said: {heard}")
    else:
        speak("I did not hear anything. Please try again.")