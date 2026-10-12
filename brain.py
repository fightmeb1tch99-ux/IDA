"""
Brain module for IDA AI Agent v5.1 — JARVIS mode
Handles NLP, command parsing, and response generation.
"""

import re
import os

from logger import log_info, log_error, log_debug, log_warning
from config import (
    LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS,
    CONTEXT_WINDOW,
)
from llm_providers import get_router


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
            r"(?:создай|сделай|создать)\s+файл\s+(.+)",
            r"новый\s+файл\s+(.+)",
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
            r"помощь|помоги|help|команды",
            r"что\s+ты\s+умеешь",
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
        if any(k in text_lower for k in ("гугли", "google", "поищи в", "найди в интернете")):
            for pattern in self.PATTERNS.get("search", []):
                match = re.search(pattern, text_lower)
                if match:
                    arg = match.group(1).strip() if match.lastindex else text_lower
                    log_debug(f"Pattern matched: tool=search, arg={arg}")
                    return "search", arg
            return "search", text_lower
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
        self.router = get_router()
        self.use_groq = self.router.is_available() and self.router.primary_name == "groq"
        self.client = self.router  # back-compat: truthy if any provider
        if not self.router.is_available():
            log_warning(
                "Нет рабочего API-ключа. Добавь GROQ_API_KEY в .env — "
                "бесплатно: https://console.groq.com/keys"
            )

    def decide_tool(self, text: str):
        return self.parser.parse(text)

    def maybe_update_profile(self, text: str) -> None:
        """Вытащить имя/город/факты из реплики пользователя."""
        import re
        low = text.lower().strip()
        m = re.search(r"меня зовут\s+([\w\-]+)", low)
        if m:
            self.memory["name"] = m.group(1).capitalize()
            self.memory.setdefault("profile", {})["name"] = self.memory["name"]
        m = re.search(r"(?:я живу в|мой город|город)\s+([\w\-\s]+?)(?:[.!?]|$)", low)
        if m:
            city = m.group(1).strip().title()
            if len(city) < 40:
                self.memory["city"] = city
                self.memory.setdefault("profile", {})["city"] = city
        m = re.search(r"запомни(?:\s+что)?\s+(.+)", low)
        if m:
            fact = m.group(1).strip()
            if fact and len(fact) < 200:
                facts = list(self.memory.get("facts") or [])
                if fact not in facts:
                    facts.append(fact)
                    self.memory["facts"] = facts[-30:]
                    self.memory.setdefault("profile", {})["facts"] = self.memory["facts"]

    def generate_response(self, user_input: str, tool_result=None) -> str:
        text_lower = user_input.lower()

        # Help
        if any(w in text_lower for w in ["помощь", "помоги", "что ты умеешь", "команды", "help"]):
            return self._get_help_message()

        # Greeting
        if re.search(r"\b(привет|хай|здравствуй|hello|hi|hey)\b", text_lower):
            name = self.memory.get("name")
            greeting = f", {name}!" if name else "!"
            return f"Привет{greeting} Я IDA — твой Джарвис. Чем помочь? 👋"

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
            if self.router.is_available():
                prompt = f"Пользователь спросил: «{user_input}». Результат: {tool_result}. Прокомментируй кратко и дружелюбно по-русски."
                return self._get_llm_response(prompt)
            return str(tool_result)

        # LLM (Groq or OpenAI)
        if self.router.is_available():
            return self._get_llm_response(user_input)

        return (
            "Нет API-ключа. Добавь GROQ_API_KEY в .env\n"
            "Бесплатно: https://console.groq.com/keys\n"
            "Или напиши «помощь» для списка локальных команд."
        )

    def add_to_history(self, user_input: str, response: str):
        self.conversation_history.append({"user": user_input, "response": response})
        # AIRI-style episodic tracking on the memory dict
        try:
            n = int(self.memory.get("turns_since_summary") or 0) + 1
            self.memory["turns_since_summary"] = n
            if n >= 8 and len(self.conversation_history) >= 4:
                recent = self.conversation_history[-8:]
                bits = []
                for e in recent:
                    u = (e.get("user") or "")[:80]
                    a = (e.get("response") or "")[:80]
                    bits.append(f"U:{u} → A:{a}")
                ep = " | ".join(bits)[:700]
                episodes = list(self.memory.get("episodes") or [])
                episodes.append({"ts": __import__("datetime").datetime.now().isoformat(), "summary": ep, "tags": []})
                self.memory["episodes"] = episodes[-30:]
                self.memory["turns_since_summary"] = 0
                self.memory["summary"] = " | ".join(x["summary"][:100] for x in episodes[-3:])
                if "profile" in self.memory and isinstance(self.memory["profile"], dict):
                    self.memory["profile"]["summary"] = self.memory["summary"]
        except Exception:
            pass

    def get_history(self):
        return self.conversation_history

    def _get_llm_response(self, user_input: str) -> str:
        try:
            profile = self.memory.get("profile") or {}
            name = profile.get("name") or self.memory.get("name") or "неизвестно"
            city = profile.get("city") or self.memory.get("city") or "не указан"
            facts = profile.get("facts") or self.memory.get("facts") or []
            facts_s = "; ".join(facts[-8:]) if facts else "нет"
            core = self.memory.get("core_memory") or []
            core_s = "; ".join(core[-10:]) if core else "нет"
            episodes = self.memory.get("episodes") or []
            ep_s = " || ".join((e.get("summary") or "")[:100] for e in episodes[-3:]) if episodes else "нет"
            summary = profile.get("summary") or self.memory.get("summary") or ""
            system_prompt = (
                "Ты — IDA, персональный ИИ-компаньон в духе ДЖАРВИСА (JARVIS). "
                "Ты живой цифровой аватар: внимательный, спокойный, чуть ироничный, всегда на стороне пользователя. "
                "Говори по-русски (можно вставлять английские термины). Кратко, по делу, без воды. "
                "Если пользователь просит действие — выполняй через доступные инструменты или четко объясни шаги. "
                "Проявляй инициативу: предлагай следующий шаг, предупреждай о рисках, напоминай о контексте. "
                "У тебя есть аватар (Live2D) и голос: отвечай так, будто говоришь вслух, живо и естественно. "
                "Не выдумывай факты. Если чего-то не знаешь — скажи прямо и предложи, как узнать. "
                f"Имя пользователя: {name}. Город: {city}.\n"
                f"Core memory: {core_s}.\n"
                f"Факты: {facts_s}.\n"
                f"Недавние эпизоды: {ep_s}.\n"
                f"Summary: {summary[:300]}.\n"
                "Версия: IDA v5.3 (multi-LLM router + memory)."
            )
            messages = [{"role": "system", "content": system_prompt}]
            for entry in self.conversation_history[-CONTEXT_WINDOW:]:
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["response"]})
            messages.append({"role": "user", "content": user_input})

            if not self.router.is_available():
                return "Нет доступных LLM сервисов."
            result = self.router.chat(
                messages,
                temperature=LLM_TEMPERATURE,
                max_tokens=LLM_MAX_TOKENS,
            )
            if result and result.content:
                return result.content
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
        return """Доступные команды IDA v5.2:

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
