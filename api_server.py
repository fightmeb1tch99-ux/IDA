#!/usr/bin/env python3
"""
IDA Unified API — один сервис на :8000
HTTP + WebSocket + профиль + TTS-хук для аватара.

Запуск:
  python api_server.py
  ./start.sh   # через launcher
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional, Set

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import FileResponse, HTMLResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("Нужно: pip install fastapi uvicorn")
    sys.exit(1)

from logger import log_error, log_info
from memory_manager import MemoryManager
from brain import Brain
from tools.tools import TOOLS

app = FastAPI(title="IDA Unified API", version="5.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_mgr = MemoryManager()
brain = Brain(memory_mgr.load())
connected: Set[WebSocket] = set()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    speak: bool = False


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    language: Optional[str] = None
    preferences: Optional[dict] = None
    facts: Optional[list] = None


def process_message(message: str) -> str:
    """Синхронная обработка через Brain + tools + профиль."""
    global brain
    try:
        brain.maybe_update_profile(message)
        tool_name, arg = brain.decide_tool(message)
        tool_result = None
        if tool_name and tool_name in TOOLS:
            try:
                fn = TOOLS[tool_name]
                tool_result = fn(arg) if arg is not None else fn()
            except Exception as e:
                tool_result = f"Ошибка инструмента: {e}"
        response = brain.generate_response(message, tool_result)
        brain.add_to_history(message, response)
        memory_mgr.save(brain.memory)
        return response
    except Exception as e:
        log_error("process_message", e)
        return f"Сбой агента: {e}"


async def broadcast(payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False)
    dead = []
    for ws in connected:
        try:
            await ws.send_text(data)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connected.discard(ws)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ida-unified",
        "version": "5.2",
        "clients": len(connected),
        "profile": memory_mgr.get_profile_public(),
    }


@app.get("/api/profile")
async def get_profile():
    return {"profile": memory_mgr.get_profile()}


@app.post("/api/profile")
async def update_profile(body: ProfileUpdate):
    profile = memory_mgr.update_profile(
        name=body.name,
        city=body.city,
        language=body.language,
        preferences=body.preferences,
        facts=body.facts,
    )
    brain.memory = memory_mgr.memory
    return {"ok": True, "profile": profile}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    msg = req.message.strip()
    if not msg:
        raise HTTPException(400, "Пустое сообщение")
    log_info(f"API chat: {msg[:80]}")
    await broadcast(
        {
            "type": "avatar_state",
            "data": {"state": "thinking", "isSpeaking": False, "isListening": False},
        }
    )
    loop = asyncio.get_event_loop()
    reply = await loop.run_in_executor(None, process_message, msg)
    await broadcast(
        {
            "type": "avatar_state",
            "data": {
                "state": "speaking",
                "isSpeaking": True,
                "isListening": False,
                "text": reply,
            },
        }
    )
    await broadcast({"type": "chat", "data": {"role": "assistant", "text": reply}})
    audio_url = None
    if req.speak:
        try:
            from voice import synthesize_to_file

            path = synthesize_to_file(reply)
            if path:
                audio_url = f"/api/tts/file?path={Path(path).name}"
        except Exception as e:
            log_error("TTS", e)
    await broadcast(
        {
            "type": "avatar_state",
            "data": {"state": "idle", "isSpeaking": False, "isListening": True},
        }
    )
    return {"response": reply, "audio_url": audio_url, "profile": memory_mgr.get_profile_public()}


@app.post("/api/tts")
async def tts_endpoint(body: dict):
    text = (body.get("text") or "").strip()
    if not text:
        raise HTTPException(400, "text required")
    try:
        from voice import synthesize_to_file

        path = synthesize_to_file(text)
        if not path:
            return {"ok": False, "error": "TTS недоступен (поставь edge-tts или pyttsx3)"}
        return {"ok": True, "url": f"/api/tts/file?path={Path(path).name}"}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/api/tts/file")
async def tts_file(path: str):
    safe = Path(path).name
    full = ROOT / "logs" / "tts" / safe
    if not full.exists():
        raise HTTPException(404, "file not found")
    media = "audio/mpeg" if safe.endswith(".mp3") else "audio/wav"
    return FileResponse(full, media_type=media)


@app.get("/api/history")
async def history():
    return {"history": brain.get_history()[-50:]}


@app.get("/api/stats")
async def stats():
    return memory_mgr.get_stats()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connected.add(ws)
    await ws.send_text(
        json.dumps(
            {
                "type": "status",
                "data": {"status": "connected", "clients": len(connected)},
            },
            ensure_ascii=False,
        )
    )
    await ws.send_text(
        json.dumps(
            {
                "type": "avatar_state",
                "data": {"state": "idle", "isSpeaking": False, "isListening": True},
            },
            ensure_ascii=False,
        )
    )
    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                msg = {"type": "chat", "message": raw}
            mtype = msg.get("type")
            if mtype == "ping":
                await ws.send_text(json.dumps({"type": "pong"}))
                continue
            user_text = (msg.get("message") or msg.get("data") or "").strip()
            if not user_text and mtype not in ("chat", None):
                continue
            if not user_text:
                continue
            await broadcast(
                {
                    "type": "avatar_state",
                    "data": {
                        "state": "thinking",
                        "isSpeaking": False,
                        "isListening": False,
                    },
                }
            )
            loop = asyncio.get_event_loop()
            reply = await loop.run_in_executor(None, process_message, user_text)
            await broadcast(
                {
                    "type": "avatar_state",
                    "data": {
                        "state": "speaking",
                        "isSpeaking": True,
                        "isListening": False,
                        "text": reply,
                    },
                }
            )
            await broadcast(
                {"type": "chat", "data": {"role": "assistant", "text": reply}}
            )
            await broadcast(
                {
                    "type": "avatar_state",
                    "data": {
                        "state": "idle",
                        "isSpeaking": False,
                        "isListening": True,
                    },
                }
            )
    except WebSocketDisconnect:
        connected.discard(ws)
    except Exception:
        connected.discard(ws)


@app.get("/", response_class=HTMLResponse)
async def root_page():
    html_path = ROOT / "web_chat.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text(encoding="utf-8"))
    return HTMLResponse(
        """<!DOCTYPE html><html><head><meta charset=utf-8><title>IDA</title></head>
<body style="font-family:system-ui;background:#0a0e1a;color:#e2e8f0;padding:2rem">
<h1>IDA Unified API</h1>
<p>POST /api/chat · WS /ws · GET /health · GET /api/profile</p>
<p><a href="/health" style="color:#38bdf8">/health</a></p>
</body></html>"""
    )


def run(host: str = "0.0.0.0", port: int = 8000):
    log_info(f"IDA Unified API → http://{host}:{port}  ws://{host}:{port}/ws")
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run()
