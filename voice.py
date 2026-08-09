"""
IDA Voice Module — unified STT / TTS with graceful fallbacks.

Current: SpeechRecognition + pyttsx3
Next: Whisper (STT) + Piper (TTS)

Usage:
    from voice import speak, listen, is_voice_available
"""

from __future__ import annotations
import os
import platform
import subprocess
from logger import log_info, log_error, log_warning

# ─── TTS ───────────────────────────────────────────────────────────
_engine = None
_tts_ready = False

def _init_tts():
    global _engine, _tts_ready
    if _tts_ready:
        return
    try:
        import pyttsx3
        _engine = pyttsx3.init()
        voices = _engine.getProperty("voices") or []
        for v in voices:
            name = (v.name or "").lower()
            if "russian" in name or "ru" in name:
                _engine.setProperty("voice", v.id)
                break
        _engine.setProperty("rate", 175)
        _tts_ready = True
        log_info("TTS (pyttsx3) ready")
    except Exception as e:
        log_warning(f"TTS init failed: {e}")


def speak(text: str) -> None:
    """Speak text. Falls back to print if TTS unavailable."""
    if not text:
        return
    clean = text.replace("**", "").replace("*", "").replace("`", "").strip()
    log_info(f"IDA says: {clean[:80]}...")

    # Termux special case
    if os.path.exists("/data/data/com.termux/files/usr/bin/termux-tts-speak"):
        try:
            subprocess.run(["termux-tts-speak", clean], check=False, timeout=30)
            return
        except Exception:
            pass

    _init_tts()
    if _engine and _tts_ready:
        try:
            _engine.say(clean)
            _engine.runAndWait()
            return
        except Exception as e:
            log_error("TTS speak error", e)

    print(f"[IDA]: {clean}")


# ─── STT ───────────────────────────────────────────────────────────
def listen(timeout: int = 5, phrase_time_limit: int = 10) -> str | None:
    """
    Listen from microphone and return text.
    Returns None on failure / silence.
    """
    try:
        import speech_recognition as sr
    except ImportError:
        log_warning("SpeechRecognition not installed")
        return None

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("[IDA] Слушаю...")
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    except Exception as e:
        log_error("Microphone error", e)
        return None

    # Try Google first (free, needs internet), then Sphinx offline
    try:
        text = r.recognize_google(audio, language="ru-RU")
        log_info(f"Recognized: {text}")
        return text
    except Exception:
        pass

    try:
        text = r.recognize_sphinx(audio)
        log_info(f"Recognized (sphinx): {text}")
        return text
    except Exception as e:
        log_warning(f"STT failed: {e}")
        return None


def is_voice_available() -> dict:
    """Return status of voice subsystems."""
    stt = False
    tts = False
    try:
        import speech_recognition
        stt = True
    except ImportError:
        pass
    try:
        import pyttsx3
        tts = True
    except ImportError:
        pass
    return {
        "stt": stt,
        "tts": tts,
        "termux_tts": os.path.exists("/data/data/com.termux/files/usr/bin/termux-tts-speak"),
        "next": "Whisper + Piper (see docs/VOICE_ROADMAP.md)",
    }


# ─── Future hooks (Whisper / Piper) ────────────────────────────────
def listen_whisper(model_size: str = "base") -> str | None:
    """Placeholder for openai-whisper / faster-whisper integration."""
    log_warning("Whisper not integrated yet. Install openai-whisper and implement here.")
    return listen()  # fallback


def speak_piper(text: str, model_path: str | None = None) -> None:
    """Placeholder for Piper TTS."""
    log_warning("Piper not integrated yet. Falling back to current TTS.")
    speak(text)
