"""
Brain module for IDA AI Agent v4.0
Handles NLP, command parsing, and response generation.
"""

import re
import os

try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    _openai_available = False

try:
    from groq import Groq
    _groq_available = True
except ImportError:
    _groq_available = False

from logger import log_info, log_error, log_debug, log_warning
from config import (
    LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS,
    OPENAI_API_KEY, OPENAI_API_BASE, CONTEXT_WINDOW,
)


class CommandParser:
    """Parses user input and maps it to tool names using regex patterns."""

    PATTERNS = {
        "time": [
            r"(?:какое|которое|скажи|напиши|покажи)?\s*время",
            r"текущее\s+время",
            r"сколько\s+(?:сейчас\s+)?времени",
            r"который\s+час",
        ],
        "date": [
            r"(?:какая|какое|скажи|напиши|покажи)?\s*(?:сегодня\s+)?дата|сегодня",
            r"какой\s+(?:сегодня\s+)?день",
            r"текущая\s+дата",
            r"какое\s+число",
        ],
        "weather": [
            r"(?:какая|как|скажи|покажи)?\s*погода",
            r"прогноз\s+погоды",
            r"температура\s+(?:на\s+улице|сегодня)",
        ],
        "calc": [
            r"посчитай\s+(.+)",
            r"вычисли\s+(.+)",
            r"сколько\s+будет\s+([\d\s\+\-\*\/\(\)\.]+)",
            r"calculate\s+(.+)",
        ],
        "create_file": [
            r"(?:создай|сделай)\s+файл\s+(.+)",
            r"сделай\s+файл\s+(.+)",
            r"create\s+file\s+(.+)",
        ],
        "search": [
            r"(?:найди|ищи|поищи)\s+(.+)",
            r"поищи\s+(.+)",
            r"поиск\s+(.+)",
            r"что\s+такое\s+(.+)",
        ],
        "run": [
            r"выполни\s+(.+)",
            r"запусти\s+(.+)",
            r"команда\s+(.+)",
        ],
        "note_add": [
            r"запомни\s+(?:что\s+)?(.+)",
            r"сохрани\s+заметку[:\s]+(.+)",
            r"заметка[:\s]+(.+)",
        ],
        "note_list": [
            r"(?:покажи|список)\s+заметки?",
            r"мои\s+заметки",
        ],
        "help": [
            r"помощь|помоги|help",
            r"help",
        ],
        "ask_kb": [
            r"(?:что\s+говорится\s+в\s+документах|найди\s+в\s+базе|спроси\s+базу)\s+(.+)",
            r"вопрос\s+по\s+файлам\s+(.+)",
            r"(?:что\s+ты\s+знаешь\s+про|расскажи\s+про|найди\s+в\s+knowledge)\s+(.+)",
            r"поиск\s+в\s+базе\s+знаний\s+(.+)",
        ],
        "stats": [
            r"статистика",
            r"мои\s+данные",
        ],
    }

    def parse(self, text: str):
        """Return (tool_name, argument) or (None, None)."""
        text_lower = text.lower().strip()
        for tool_name, patterns in self.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    arg = match.group(1).strip() if match.lastindex else None
                    log_debug(f"Pattern matched: tool={tool_name}, arg={arg}")
                    return tool_name, arg
        return None, None


class Brain:
    """Core reasoning module for IDA."""

    def __init__(self, memory: dict):
        self.memory = memory
        self.conversation_history = []
        self.parser = CommandParser()
        self.client = None
        self.groq_client = None
        self.use_groq = False

        # Try Groq first (free, recommended for Termux)
        groq_key = (os.getenv("GROQ_API_KEY") or "").strip()
        if _groq_available and groq_key and groq_key.startswith("gsk_"):
            try:
                self.groq_client = Groq(api_key=groq_key)
                self.use_groq = True
                log_info("Groq client OK (free LLM)")
            except Exception as e:
                log_error("Failed to initialize Groq client", e)
                self.use_groq = False
        elif groq_key and not groq_key.startswith("gsk_"):
            log_warning("GROQ_API_KEY выглядит неправильно (должен начинаться с gsk_)")

        # Fallback to OpenAI only if Groq not available
        if not self.use_groq and _openai_available:
            api_key = (OPENAI_API_KEY or os.getenv("OPENAI_API_KEY") or "").strip()
            api_base = OPENAI_API_BASE or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
            # Skip obvious placeholders / empty
            if api_key and api_key not in ("sk-...", "sk-proj-...", "your_key_here") and len(api_key) > 20:
                try:
                    self.client = OpenAI(api_key=api_key, base_url=api_base)
                    log_info(f"OpenAI client initialized (model: {LLM_MODEL})")
                except Exception as e:
                    log_error("Failed to initialize OpenAI client", e)
            else:
                log_warning(
                    "Нет рабочего API-ключа. Добавь GROQ_API_KEY в .env — "
                    "бесплатно: https://console.groq.com/keys"
                )

    def decide_tool(self, text: str):
        return self.parser.parse(text)

    def generate_response(self, user_input: str, tool_result=None) -> str:
        text_lower = user_input.lower()

        # Help
        if any(w in text_lower for w in ["помощь", "помоги", "что ты умеешь", "команды", "help"]):
            return self._get_help_message()

        # Greeting
        if re.search(r"\b(привет|хай|здравствуй|hello|hi|hey)\b", text_lower):
            name = self.memory.get("name")
            greeting = f", {name}!" if name else "!"
            return f"Привет{greeting} Я IDA v4.0. Чем могу помочь? 👋"

        # Remember name
        m = re.search(r"меня зовут\s+(\S+)", text_lower)
        if m:
            name = m.group(1).capitalize()
            self.memory["name"] = name
            return f"Отлично, запомнил: **{name}** Рад познакомиться!"

        # What is my name
        if re.search(r"как\s+меня\s+зовут", text_lower):
            name = self.memory.get("name")
            return f"Тебя зовут **{name}**" if name else "Я пока не знаю твоё имя. Скажи: «Меня зовут [имя]»"

        # Tool result
        if tool_result is not None:
            if self.use_groq or self.client:
                prompt = f"Пользователь спросил: «{user_input}». Результат: {tool_result}. Прокомментируй кратко и дружелюбно по-русски."
                return self._get_llm_response(prompt)
            return str(tool_result)

        # LLM (Groq or OpenAI)
        if self.use_groq or self.client:
            return self._get_llm_response(user_input)

        return (
            "Нет API-ключа. Добавь GROQ_API_KEY в .env\n"
            "Бесплатно: https://console.groq.com/keys\n"
            "Или напиши «помощь» для списка локальных команд."
        )

    def add_to_history(self, user_input: str, response: str):
        self.conversation_history.append({"user": user_input, "response": response})

    def get_history(self):
        return self.conversation_history

    def _get_llm_response(self, user_input: str) -> str:
        try:
            system_prompt = (
                f"Ты — IDA (Инновационный динамический помощник) v4.0. "
                f"Отвечай по-русски, кратко и дружелюбно. "
                f"Имя пользователя: {self.memory.get('name', 'неизвестно')}."
            )
            messages = [{"role": "system", "content": system_prompt}]
            for entry in self.conversation_history[-CONTEXT_WINDOW:]:
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["response"]})
            messages.append({"role": "user", "content": user_input})

            # Use Groq if available
            if self.use_groq and self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024,
                )
            # Fallback to OpenAI
            elif self.client:
                response = self.client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=messages,
                    temperature=LLM_TEMPERATURE,
                    max_tokens=LLM_MAX_TOKENS,
                )
            else:
                return "Нет доступных LLM сервисов."
            
            if response and response.choices:
                return response.choices[0].message.content.strip()
            return "Извини, не смог получить ответ."
        except Exception as e:
            log_error("LLM Error", e)
            err = str(e)
            if "401" in err or "invalid_api_key" in err or "Incorrect API key" in err:
                return (
                    "❌ Неверный API-ключ.\n\n"
                    "Для Termux сделай так:\n"
                    "1) nano .env\n"
                    "2) Добавь строку: GROQ_API_KEY=gsk_твой_ключ\n"
                    "3) Ключ бесплатно: https://console.groq.com/keys\n"
                    "4) Удали или закомментируй битый OPENAI_API_KEY\n"
                    "5) python main.py"
                )
            return f"Ошибка LLM: {err}"

    def _get_help_message(self) -> str:
        return """Доступные команды IDA v4.0:

Время и дата:
  - «Какое время?» — текущее время
  - «Какая дата?» — текущая дата

Погода:
  - «Какая погода?» — текущая погода

Калькулятор:
  - «Посчитай 15 * 7 + 3» — результат

Файлы:
  - «Создай файл notes.txt» — создать файл

Поиск:
  - «Найди Python туториал» — поиск

Заметки:
  - «Запомни купить молоко» — сохранить заметку
  - «Покажи заметки» — список заметок

Команды:
  - «Выполни ls» — безопасная команда

Личное:
  - «Меня зовут [имя]» — сохранить имя
  - «Как меня зовут?» — узнать имя

Прочее:
  - «Статистика» — данные о сессии
  - «Выход» / «quit» — завершить работу"""
