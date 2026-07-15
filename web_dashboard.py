"""
IDA Web Dashboard & Chat — Full Web Interface
FastAPI server for web-based chat and management.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from dotenv import load_dotenv
from memory_manager import MemoryManager
from brain import Brain
from tools.tools import TOOLS
from logger import log_info, log_error

load_dotenv()

app = FastAPI(title="IDA Web Chat")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize IDA
memory_mgr = MemoryManager()
memory = memory_mgr.load()
brain = Brain(memory)

@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    """Serve the web chat interface."""
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
    """Process chat messages and return responses."""
    try:
        message = request.get("message", "").strip()
        if not message:
            return {"error": "Сообщение не может быть пустым"}

        log_info(f"Web Chat: {message}")

        # 1. Decide if a tool is needed
        tool_name, tool_arg = brain.decide_tool(message)
        
        tool_result = None
        if tool_name and tool_name in TOOLS:
            try:
                tool_result = TOOLS[tool_name](tool_arg) if tool_arg else TOOLS[tool_name]()
            except Exception as e:
                tool_result = f"Ошибка инструмента: {str(e)}"

        # 2. Generate final response
        response = brain.generate_response(message, tool_result)
        
        # 3. Update memory
        brain.add_to_history(message, response)
        memory_mgr.save()
        
        return {"response": response}
    except Exception as e:
        log_error("Chat error", e)
        return {"error": str(e)}

@app.get("/api/notes")
async def get_notes():
    """Get all notes."""
    try:
        notes = memory.get("notes", [])
        return {"notes": notes}
    except Exception as e:
        log_error("Failed to fetch notes", e)
        return {"error": str(e)}

@app.get("/api/history")
async def get_history():
    """Get chat history."""
    try:
        history = memory.get("history", [])
        return {"history": history[-50:]}  # Last 50 messages
    except Exception as e:
        log_error("Failed to fetch history", e)
        return {"error": str(e)}

@app.get("/api/stats")
async def get_stats():
    """Get usage statistics."""
    try:
        history = memory.get("history", [])
        notes = memory.get("notes", [])
        return {
            "total_messages": len(history),
            "total_notes": len(notes),
            "status": "online"
        }
    except Exception as e:
        log_error("Failed to compute stats", e)
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🌐 IDA Web Chat starting on http://localhost:8000")
    print("📱 Access from browser: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
