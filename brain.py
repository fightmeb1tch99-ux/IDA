"""
Brain module for IDA AI Agent v2.5 (Optimized)
Handles NLP, command parsing, and response generation with lazy initialization.
"""

import re
import os
from logger import log_info, log_error, log_debug, log_warning
from config import (
    LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS,
    OPENAI_API_KEY, OPENAI_API_BASE, CONTEXT_WINDOW,
)

class CommandParser:
    """Parses user input and maps it to tool names using regex patterns."""
    PATTERNS = {
        "time": [r"(?:какое|которое|скажи|напиши|покажи)?\s*время", r"текущее\s+время", r"сколько\s+(?:сейчас\s+)?времени", r"который\s+час"],
        "date": [r"(?:какая|какое|скажи|напиши|покажи)?\s*(?:сегодня\s+)?дата|сегодня", r"какой\s+(?:сегодня\s+)?день", r"текущая\s+дата", r"какое\s+число"],
        "weather": [r"(?:какая|как|скажи|покажи)?\s*погода", r"прогноз\s+погоды", r"температура\s+(?:на\s+улице|сегодня)"],
        "calc": [r"посчитай\s+(.+)", r"вычисли\s+(.+)", r"сколько\s+будет\s+([\d\s\+\-\*\/\(\)\.]+)", r"calculate\s+(.+)"],
        "create_file": [r"(?:создай|сделай)\s+файл\s+(.+)", r"сделай\s+файл\s+(.+)", r"create\s+file\s+(.+)"],
        "search": [r"(?:найди|ищи|поищи)\s+(.+)", r"поищи\s+(.+)", r"поиск\s+(.+)", r"что\s+такое\s+(.+)"],
        "run": [r"выполни\s+(.+)", r"запусти\s+(.+)", r"команда\s+(.+)"],
        "note_add": [r"запомни\s+(?:what\s+)?(.+)", r"сохрани\s+заметку[:\s]+(.+)", r"заметка[:\s]+(.+)"],
        "note_list": [r"(?:покажи|список)\s+заметки?", r"мои\s+заметки"],
        "help": [r"помощь|помоги|help"],
        "draw": [r"(?:нарисуй|создай\s+картинку|изобрази)\s+(.+)", r"картинка\s+(.+)"],
        "remind": [r"(?:напомни|напомни\s+мне)\s+(?:через\s+)?(\d+)\s+(?:минут|минуты|мин)\s+(.+)", r"(?:напомни|напомни\s+мне)\s+(.+)\s+(?:через\s+)?(\d+)\s+(?:минут|минуты|мин)"],
        "ask_kb": [r"(?:что\s+говорится\s+в\s+документах|найди\s+в\s+базе|спроси\s+базу)\s+(.+)", r"вопрос\s+по\s+файлам\s+(.+)"],
        "stats": [r"статистика", r"мои\s+данные"],
    }

    def parse(self, text: str):
        text_lower = text.lower().strip()
        for tool_name, patterns in self.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    arg = match.group(1).strip() if match.lastindex else None
                    return tool_name, arg
        return None, None

class Brain:
    """Core reasoning module for IDA with lazy OpenAI init."""
    def __init__(self, memory: dict):
        self.memory = memory
        self.conversation_history = []
        self.parser = CommandParser()
        self.client = None

    def _get_client(self):
        """Lazy initialize OpenAI client only when needed."""
        if self.client is None:
            try:
                from openai import OpenAI
                api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
                api_base = OPENAI_API_BASE or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
                if api_key:
                    self.client = OpenAI(api_key=api_key, base_url=api_base)
                    log_info(f"OpenAI client lazy-initialized (model: {LLM_MODEL})")
                else:
                    log_warning("OPENAI_API_KEY not set — using rule-based fallback")
            except Exception as e:
                log_error("Failed to initialize OpenAI client", e)
        return self.client

    def decide_tool(self, text: str):
        return self.parser.parse(text)

    def generate_response(self, user_input: str, tool_result=None) -> str:
        text_lower = user_input.lower()
        if any(w in text_lower for w in ["помощь", "помоги", "что ты умеешь", "команды", "help"]):
            return self._get_help_message()
        if re.search(r"\b(привет|хай|здравствуй|hello|hi|hey)\b", text_lower):
            name = self.memory.get("name")
            greeting = f", {name}!" if name else "!"
            return f"Привет{greeting} Я IDA v2.5. Чем могу помочь? 👋"

        client = self._get_client()
        if tool_result is not None:
            if client:
                prompt = f"Пользователь спросил: «{user_input}». Результат: {tool_result}. Прокомментируй кратко и дружелюбно."
                return self._get_llm_response(prompt)
            return str(tool_result)

        if client:
            return self._get_llm_response(user_input)
        return "Я пока не понимаю это. Напиши «помощь» для списка команд."

    def _get_llm_response(self, user_input: str) -> str:
        try:
            client = self._get_client()
            system_prompt = f"Ты — IDA v2.5. Отвечай по-русски, кратко и дружелюбно. Пользователь: {self.memory.get('name', 'бро')}."
            messages = [{"role": "system", "content": system_prompt}]
            for entry in self.conversation_history[-CONTEXT_WINDOW:]:
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["response"]})
            messages.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(model=LLM_MODEL, messages=messages, temperature=LLM_TEMPERATURE, max_tokens=LLM_MAX_TOKENS)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Ошибка LLM: {str(e)}"

    def add_to_history(self, user_input: str, response: str):
        self.conversation_history.append({"user": user_input, "response": response})

    def _get_help_message(self) -> str:
        return "Доступные команды: Время, Погода, Калькулятор, Заметки, Файлы, Поиск, Напоминания, Рисование, Зрение (пришли фото)."
