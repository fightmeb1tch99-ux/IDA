import datetime
import subprocess
import urllib.request
import json


def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def create_file(filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")
    return f"Файл {filename} создан"


def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip() if result else "Готово"
    except Exception as e:
        return f"Ошибка: {str(e)}"


def web_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())

        abstract = data.get("AbstractText")
        if abstract:
            return abstract

        related = data.get("RelatedTopics", [])
        if related:
            return related[0].get("Text", "Нет точного ответа")

        return "Ничего не найдено 🤷"
    except Exception as e:
        return f"Ошибка интернета: {str(e)}"


TOOLS = {
    "time": get_time,
    "date": get_date,
    "create_file": create_file,
    "run": run_command,
    "search": web_search,
}
