"""
IDA Web Dashboard — Control Panel
FastAPI server for managing IDA, viewing notes, and chat history.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from memory_manager import MemoryManager
from brain import Brain

load_dotenv()

app = FastAPI(title="IDA Dashboard")

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
async def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IDA Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #fff; min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            header { text-align: center; margin-bottom: 40px; }
            h1 { font-size: 3em; margin-bottom: 10px; background: linear-gradient(45deg, #00d4ff, #0099ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; padding: 20px; backdrop-filter: blur(10px); }
            .card h2 { margin-bottom: 15px; color: #00d4ff; }
            .card-content { max-height: 300px; overflow-y: auto; }
            .note { background: rgba(0, 212, 255, 0.1); padding: 10px; margin: 5px 0; border-left: 3px solid #00d4ff; border-radius: 5px; }
            .chat-msg { margin: 10px 0; padding: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px; }
            .user-msg { border-left: 3px solid #0099ff; }
            .ida-msg { border-left: 3px solid #00d4ff; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); color: #fff; border-radius: 5px; }
            button { background: linear-gradient(45deg, #00d4ff, #0099ff); color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
            button:hover { opacity: 0.9; }
            .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; }
            .stat-box { background: rgba(0, 212, 255, 0.2); padding: 15px; border-radius: 5px; text-align: center; }
            .stat-box .number { font-size: 2em; color: #00d4ff; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🤖 IDA Dashboard</h1>
                <p>Твоя личная панель управления ИИ-помощником</p>
            </header>

            <div class="stats">
                <div class="stat-box">
                    <div class="number" id="notes-count">0</div>
                    <p>Заметок</p>
                </div>
                <div class="stat-box">
                    <div class="number" id="chat-count">0</div>
                    <p>Сообщений</p>
                </div>
                <div class="stat-box">
                    <div class="number" id="uptime">0h</div>
                    <p>Активна</p>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <h2>📝 Твои Заметки</h2>
                    <div class="card-content" id="notes-list"></div>
                </div>

                <div class="card">
                    <h2>💬 История Чата</h2>
                    <div class="card-content" id="chat-history"></div>
                </div>

                <div class="card">
                    <h2>✉️ Новое Сообщение</h2>
                    <textarea id="message-input" placeholder="Напиши что-нибудь..."></textarea>
                    <button onclick="sendMessage()">Отправить</button>
                </div>
            </div>
        </div>

        <script>
            async function loadData() {
                const notes = await fetch('/api/notes').then(r => r.json());
                const history = await fetch('/api/history').then(r => r.json());
                
                document.getElementById('notes-count').textContent = notes.length;
                document.getElementById('chat-count').textContent = history.length;
                
                const notesList = document.getElementById('notes-list');
                notesList.innerHTML = notes.map(n => `<div class="note">${n}</div>`).join('');
                
                const chatDiv = document.getElementById('chat-history');
                chatDiv.innerHTML = history.map((msg, i) => 
                    `<div class="chat-msg ${i % 2 === 0 ? 'user-msg' : 'ida-msg'}">${msg}</div>`
                ).join('');
            }

            async function sendMessage() {
                const input = document.getElementById('message-input');
                const msg = input.value;
                if (!msg) return;
                
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                const result = await response.json();
                input.value = '';
                loadData();
            }

            loadData();
            setInterval(loadData, 5000);
        </script>
    </body>
    </html>
    """

@app.get("/api/notes")
async def get_notes():
    try:
        notes = memory.get("notes", [])
        return notes
    except:
        return []

@app.get("/api/history")
async def get_history():
    try:
        history = memory.get("history", [])
        return [f"{msg['role']}: {msg['content'][:50]}..." for msg in history[-20:]]
    except:
        return []

@app.post("/api/chat")
async def chat(request: dict):
    try:
        message = request.get("message", "")
        response = brain.generate_response(message, None)
        brain.add_to_history(message, response)
        memory_mgr.save(memory)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🌐 IDA Web Dashboard starting on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
