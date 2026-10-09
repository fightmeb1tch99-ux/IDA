"""
IDA Web Dashboard & Chat — Full Web Interface
FastAPI server for web-based chat and management.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from memory_manager import MemoryManager
from brain import Brain
from tools.tools import TOOLS, list_notes
from logger import log_info, log_error

app = FastAPI(title="IDA Web Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_mgr = MemoryManager()
brain = Brain(memory_mgr.memory)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ida-web"}


@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    try:
        with open("web_chat.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body style="background: #0f0c29; color: #fff; text-align: center; padding: 50px;">
                <h1>🤖 IDA Web Chat</h1>
                <p>Интерфейс загружается...</p>
            </body>
        </html>
        """


@app.post("/api/chat")
async def chat(request: dict):
    try:
        message = request.get("message", "").strip()
        if not message:
            return {"error": "Сообщение не может быть пустым"}

        log_info(f"Web Chat: {message}")

        tool_name, tool_arg = brain.decide_tool(message)

        tool_result = None
        if tool_name and tool_name in TOOLS:
            try:
                tool_fn = TOOLS[tool_name]
                if tool_arg is not None:
                    tool_result = tool_fn(tool_arg)
                else:
                    tool_result = tool_fn()
            except TypeError:
                try:
                    tool_result = TOOLS[tool_name](tool_arg) if tool_arg else TOOLS[tool_name]()
                except Exception as e:
                    tool_result = f"Ошибка инструмента: {e}"
            except Exception as e:
                tool_result = f"Ошибка инструмента: {e}"

        response = brain.generate_response(message, tool_result)
        brain.add_to_history(message, response)

        if "history" not in brain.memory:
            brain.memory["history"] = []
        brain.memory["history"].append({"user": message, "response": response})
        brain.memory["history"] = brain.memory["history"][-200:]

        memory_mgr.save(brain.memory)

        return {"response": response}
    except Exception as e:
        log_error("Chat error", e)
        return {"error": "Внутренняя ошибка сервера"}


@app.get("/api/notes")
async def get_notes():
    try:
        raw = list_notes()
        return {"notes": raw}
    except Exception as e:
        log_error("Notes error", e)
        return {"error": "Не удалось загрузить заметки"}


@app.get("/api/history")
async def get_history():
    try:
        history = brain.memory.get("history") or [
            {"user": h.get("user"), "response": h.get("response")}
            for h in brain.get_history()
        ]
        return {"history": history[-50:]}
    except Exception as e:
        log_error("History error", e)
        return {"error": "Не удалось загрузить историю"}


@app.get("/api/stats")
async def get_stats():
    try:
        history = brain.memory.get("history") or brain.get_history()
        notes_text = list_notes()
        notes_count = 0 if "Заметок пока нет" in notes_text else notes_text.count("\n  ")
        return {
            "total_messages": len(history),
            "total_notes": notes_count,
            "status": "online",
            "version": "4.1",
        }
    except Exception as e:
        log_error("Stats error", e)
        return {"error": "Не удалось получить статистику"}


if __name__ == "__main__":
    import uvicorn
    print("IDA Web Chat starting on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
