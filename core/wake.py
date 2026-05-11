# ============================================================
# BREACH — core/wake.py
# Wake word detection — listens for "Hey BREACH" in background
# Always running, zero CPU impact, 100% local
# ============================================================

import os
import struct
import pvporcupine
from pvrecorder import PvRecorder
from dotenv import load_dotenv

load_dotenv()


def wait_for_wake_word():
    """
    Blocks until the wake word "Hey BREACH" (or "computer") is detected.
    Uses Picovoice Porcupine — runs fully offline on CPU.
    Returns True when wake word heard.
    """
    access_key = os.getenv("PICOVOICE_KEY")

    if not access_key or access_key == "your_picovoice_key_here":
        # No wake word key — skip wake word, always listen
        print("  [!] No PICOVOICE_KEY found — wake word disabled")
        print("  [→] Running in direct listen mode")
        return True

    try:
        # Use built-in "computer" keyword (free, no custom model needed)
        # You can change to "hey siri", "alexa", "hey google" etc
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=["computer"]   # says "computer" to activate
        )

        recorder = PvRecorder(
            frame_length=porcupine.frame_length,
            device_index=-1   # default microphone
        )

        print("  [→] Wake word active — say 'Computer' to activate BREACH")
        recorder.start()

        try:
            while True:
                pcm        = recorder.read()
                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("  [✓] Wake word detected!")
                    return True
        finally:
            recorder.stop()
            recorder.delete()
            porcupine.delete()

    except Exception as e:
        print(f"  [!] Wake word error: {e}")
        print("  [→] Falling back to direct listen mode")
        return True