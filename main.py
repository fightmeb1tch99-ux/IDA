import json
import os
from tools.tools import TOOLS

MEMORY_FILE = "memory/memory.json"


# ---------- MEMORY ----------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_memory(memory):
    os.makedirs("memory", exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


# ---------- BRAIN ----------
def decide_tool(text):
    text = text.lower()

    if "время" in text:
        return ("time", None)

    if "дата" in text:
        return ("date", None)

    if "создай файл" in text:
        filename = text.replace("создай файл", "").strip()
        return ("create_file", filename)

    if "выполни" in text:
        cmd = text.replace("выполни", "").strip()
        return ("run", cmd)

    if "найди" in text or "поиск" in text:
        query = text.replace("найди", "").replace("поиск", "").strip()
        return ("search", query)

    return (None, None)


def think(text, memory):
    tool_name, arg = decide_tool(text)

    if tool_name and tool_name in TOOLS:
        tool = TOOLS[tool_name]
        return tool(arg) if arg else tool()

    if "привет" in text.lower():
        return "Йо 👋"

    if "как меня зовут" in text.lower():
        return f"Тебя зовут {memory.get('name', 'я не знаю 😅')}"

    if "меня зовут" in text.lower():
        name = text.replace("меня зовут", "").strip()
        memory["name"] = name
        return f"Ок, запомнил: {name}"

    return "Я пока не понимаю это 🤖"


# ---------- RUN ----------
def run():
    memory = load_memory()

    print("AI Agent started 🚀 (FULL MODE)")
    print("Напиши что-нибудь\n")

    while True:
        user_input = input("Ты: ")
        response = think(user_input, memory)
        print("AI:", response)
        save_memory(memory)


if __name__ == "__main__":
    run()
