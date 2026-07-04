"""
IDA System Module — Voice & OS Integration
Handles voice recognition, text-to-speech, and system commands.
"""

import os
import sys
import time
import platform
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3
from brain import Brain
from memory_manager import MemoryManager
from tools.tools import TOOLS
from logger import log_info, log_error, log_warning

# Initialize IDA core
memory_mgr = MemoryManager()
memory = memory_mgr.load()
brain = Brain(memory)

# Initialize TTS (Text-to-Speech)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Set to Russian if available
for voice in voices:
    if 'russian' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 180) # Speed of speech

class SystemController:
    """Controls OS-level functions for IDA."""
    def __init__(self):
        self.os_type = platform.system()

    def open_app(self, app_name):
        try:
            if self.os_type == "Windows":
                os.startfile(app_name)
            elif self.os_type == "Darwin":  # macOS
                subprocess.run(["open", "-a", app_name])
            else:  # Linux/Termux
                subprocess.run(["xdg-open", app_name])
            return f"Открываю {app_name}, бро."
        except Exception as e:
            return f"Не удалось открыть {app_name}."

    def search_web(self, query):
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Ищу «{query}» в сети."

controller = SystemController()

def speak(text):
    """Speak text using TTS or Termux-TTS."""
    log_info(f"IDA says: {text}")
    
    # Check if running in Termux
    if os.path.exists('/data/data/com.termux/files/usr/bin/termux-tts-speak'):
        subprocess.run(['termux-tts-speak', text])
    else:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            log_error("TTS error", e)
            print(f"[IDA]: {text}")

def listen():
    """Listen for voice input and return as text."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\n[IDA] Слушаю...")
            r.pause_threshold = 0.8
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

        print("[IDA] Распознаю...")
        query = r.recognize_google(audio, language='ru-RU')
        print(f"[Вы] {query}")
        return query
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        log_error("Voice recognition error", e)
        return None

def process_command(query):
    """Process text query and return response."""
    if not query:
        return None
    
    query_lower = query.lower()

    # System commands integration
    if "открой" in query_lower:
        app = query_lower.replace("открой", "").strip()
        return controller.open_app(app)
    
    if "найди в интернете" in query_lower:
        search_q = query_lower.replace("найди в интернете", "").strip()
        return controller.search_web(search_q)

    # 1. Decide if a tool is needed
    tool_name, tool_arg = brain.decide_tool(query)
    
    tool_result = None
    if tool_name and tool_name in TOOLS:
        try:
            tool_result = TOOLS[tool_name](tool_arg) if tool_arg else TOOLS[tool_name]()
        except Exception as e:
            tool_result = f"Ошибка: {str(e)}"

    # 2. Generate final response
    response = brain.generate_response(query, tool_result)
    
    # 3. Update memory
    brain.add_to_history(query, response)
    memory_mgr.save()
    
    return response

def main():
    speak("Система ИДА активирована. Я слушаю тебя, бро.")
    
    while True:
        try:
            query = listen()
            if query:
                if any(word in query.lower() for word in ["выход", "пока", "отключись", "стоп"]):
                    speak("Отключаюсь. До связи, бро!")
                    break
                
                response = process_command(query)
                if response:
                    # Strip markdown for better speech
                    clean_response = response.replace("**", "").replace("*", "").replace("`", "")
                    speak(clean_response)
            
        except KeyboardInterrupt:
            speak("Система остановлена.")
            break
        except Exception as e:
            log_error("Main loop error", e)
            # speak("Произошла ошибка в системе.") # Don't speak on every error to avoid loops
            time.sleep(2)

if __name__ == "__main__":
    main()
