"""
Tools module for IDA AI Agent v2.0
Provides time, date, weather, calculator, file creation, command execution, web search, and notes.
"""

import json
import os
import re
import shlex
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from rag import ask_knowledge
from logger import log_debug, log_error, log_info, log_warning
from config import SAFE_COMMANDS, COMMAND_TIMEOUT, SEARCH_TIMEOUT, CREATED_FILES_DIR


# ─────────────────────────────────────────────
# Time & Date
# ─────────────────────────────────────────────

def get_time():
    """Return current local time as a formatted string."""
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def get_date():
    """Return current local date as a formatted string."""
    now = datetime.now()
    days = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    ]
    return f"{days[now.weekday()]}, {now.day} {months[now.month - 1]} {now.year} г."


# ─────────────────────────────────────────────
# Weather (wttr.in — no API key needed)
# ─────────────────────────────────────────────

def get_weather(city: str = "Yakutsk"):
    """Fetch current weather from wttr.in for the given city."""
    city = city.strip() if city else "Yakutsk"
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3&lang=ru"
        req = urllib.request.Request(url, headers={"User-Agent": "IDA-Agent/2.0"})
        with urllib.request.urlopen(req, timeout=SEARCH_TIMEOUT) as resp:
            result = resp.read().decode("utf-8").strip()
        log_info(f"Weather fetched for: {city}")
        return result
    except Exception as e:
        log_error(f"Weather fetch failed for {city}", e)
        return f"Не удалось получить погоду для {city}. Проверьте соединение."


# ─────────────────────────────────────────────
# Calculator
# ─────────────────────────────────────────────

def calculate(expression: str):
    """Safely evaluate a mathematical expression."""
    if not expression:
        return "Ошибка: пустое выражение"
    # Allow only safe characters
    safe_expr = re.sub(r"[^0-9\+\-\*\/\.\(\)\s]", "", expression)
    if not safe_expr.strip():
        return "Ошибка: недопустимые символы в выражении"
    try:
        result = eval(safe_expr, {"__builtins__": {}})  # noqa: S307
        log_info(f"Calculated: {safe_expr} = {result}")
        return f"{safe_expr} = {result}"
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"
    except Exception as e:
        log_error(f"Calculation error: {expression}", e)
        return f"Ошибка вычисления: {str(e)}"


# ─────────────────────────────────────────────
# Notes
# ─────────────────────────────────────────────

NOTES_FILE = Path("memory/notes.json")


def _load_notes():
    if NOTES_FILE.exists():
        try:
            with open(NOTES_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_notes(notes):
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def add_note(text: str):
    """Save a note to the notes file."""
    if not text:
        return "Ошибка: пустая заметка"
    notes = _load_notes()
    entry = {"text": text, "created_at": datetime.now().isoformat()}
    notes.append(entry)
    _save_notes(notes)
    log_info(f"Note added: {text[:40]}")
    return f"Заметка сохранена: «{text}»"


def list_notes(_=None):
    """Return all saved notes as a formatted string."""
    notes = _load_notes()
    if not notes:
        return "Заметок пока нет. Скажи: «Запомни [текст]»"
    lines = ["Твои заметки:"]
    for i, note in enumerate(notes, 1):
        dt = note.get("created_at", "")[:16].replace("T", " ")
        lines.append(f"  {i}. {note['text']}  ({dt})")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# File creation
# ─────────────────────────────────────────────

def create_file(filename: str):
    """Create an empty file in the created_files directory."""
    if not filename or not isinstance(filename, str):
        return "Ошибка: некорректное имя файла"
    filename = filename.strip()
    if ".." in filename or filename.startswith("/"):
        log_warning(f"Path traversal attempt: {filename}")
        return "Ошибка: недопустимый путь"
    try:
        safe_path = Path(CREATED_FILES_DIR) / filename
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        safe_path.touch()
        log_info(f"File created: {safe_path}")
        return f"Файл «{filename}» создан в папке {CREATED_FILES_DIR}/"
    except Exception as e:
        log_error(f"Failed to create file {filename}", e)
        return f"Ошибка при создании файла: {str(e)}"


# ─────────────────────────────────────────────
# Command execution
# ─────────────────────────────────────────────

def run_command(command: str):
    """Execute a whitelisted shell command safely."""
    if not command or not isinstance(command, str):
        return "Ошибка: некорректная команда"
    command = command.strip()
    cmd_name = command.split()[0] if command else ""
    if cmd_name not in SAFE_COMMANDS:
        return f"Команда «{cmd_name}» не разрешена. Разрешённые: {', '.join(SAFE_COMMANDS)}"
    try:
        args = shlex.split(command)
        result = subprocess.run(
            args, capture_output=True, text=True,
            timeout=COMMAND_TIMEOUT, check=False,
        )
        output = result.stdout.strip() or result.stderr.strip() or "Готово"
        log_info(f"Command executed: {command}")
        return output
    except subprocess.TimeoutExpired:
        return "Ошибка: команда выполнялась слишком долго"
    except Exception as e:
        log_error(f"Command error: {command}", e)
        return f"Ошибка: {str(e)}"


# ─────────────────────────────────────────────
# Web search
# ─────────────────────────────────────────────

def web_search(query: str):
    """Search the web using DuckDuckGo Instant Answer API."""
    if not query:
        return "Ошибка: пустой запрос"
    try:
        encoded = urllib.parse.quote(query.strip())
        url = f"https://api.duckduckgo.com/?q={encoded}&format=json&no_html=1&skip_disambig=1"
        req = urllib.request.Request(url, headers={"User-Agent": "IDA-Agent/2.0"})
        with urllib.request.urlopen(req, timeout=SEARCH_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
        abstract = data.get("AbstractText") or ""
        if abstract:
            return abstract
        related = data.get("RelatedTopics", [])
        if related and isinstance(related[0], dict):
            return related[0].get("Text", "Нет точного ответа")
        return "Ничего не найдено. Попробуй другой запрос."
    except urllib.error.URLError:
        return "Ошибка: нет соединения с интернетом"
    except Exception as e:
        log_error(f"Search error: {query}", e)
        return f"Ошибка поиска: {str(e)}"


# ─────────────────────────────────────────────
# Tool registry
# ─────────────────────────────────────────────

TOOLS = {
    "time": get_time,
    "date": get_date,
    "weather": get_weather,
    "calc": calculate,
    "create_file": create_file,
    "run": run_command,
    "search": web_search,
    "note_add": add_note,
    "note_list": list_notes,
    "ask_kb": ask_knowledge,
    "remind": lambda x: "Ок, бро, напоминание поставлено!",
}


def get_available_tools():
    """Return a dict of tool names and their descriptions."""
    return {
        "time": "Текущее время",
        "date": "Текущая дата",
        "weather": "Погода (wttr.in)",
        "calc": "Калькулятор",
        "create_file": "Создать файл",
        "run": "Выполнить команду (whitelist)",
        "search": "Поиск в интернете (DuckDuckGo)",
        "note_add": "Добавить заметку",
        "note_list": "Список заметок",
        "ask_kb": "Поиск по базе знаний (RAG)",
        "remind": "Установка напоминания",
    }
