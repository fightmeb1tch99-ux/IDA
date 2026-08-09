"""
IDA Realtime Bridge
WebSocket bridge between Python agent and Web Dashboard / mobile.

Run:
  pip install fastapi uvicorn websockets
  python -m realtime.bridge

Endpoints:
  WS  /ws          — bidirectional chat + status
  GET /health      — health check
  POST /chat       — simple HTTP fallback
"""

from __future__ import annotations
import asyncio
import json
import sys
from pathlib import Path
from typing import Set

# Make project root importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False
    print("Missing deps. Run: pip install fastapi uvicorn websockets")

if _AVAILABLE:
    app = FastAPI(title="IDA Realtime Bridge", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    connected: Set[WebSocket] = set()

    class ChatRequest(BaseModel):
        message: str
        history: list | None = None

    def _get_brain():
        """Lazy init of Brain to avoid heavy imports at startup."""
        from brain import Brain
        from memory_manager import MemoryManager
        mem = MemoryManager().load()
        return Brain(mem)

    def _process(message: str) -> str:
        try:
            from tools.tools import TOOLS
            brain = _get_brain()
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
            try:
                from memory_manager import MemoryManager
                MemoryManager().save(brain.memory)
            except Exception:
                pass
            return response
        except Exception as e:
            return f"Ошибка агента: {e}"

    async def broadcast(payload: dict):
        dead = []
        data = json.dumps(payload, ensure_ascii=False)
        for ws in connected:
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            connected.discard(ws)

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        connected.add(ws)
        await ws.send_text(json.dumps({
            "type": "status",
            "data": {"status": "connected", "clients": len(connected)}
        }, ensure_ascii=False))
        try:
            while True:
                raw = await ws.receive_text()
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    msg = {"type": "chat", "message": raw}

                if msg.get("type") == "chat" or "message" in msg:
                    user_text = msg.get("message") or msg.get("data") or ""
                    # Notify clients that IDA is thinking
                    await broadcast({"type": "status", "data": {"speaking": False, "thinking": True}})
                    # Run agent in thread to not block event loop
                    loop = asyncio.get_event_loop()
                    reply = await loop.run_in_executor(None, _process, user_text)
                    await broadcast({
                        "type": "chat",
                        "data": {"role": "assistant", "text": reply}
                    })
                    await broadcast({"type": "status", "data": {"thinking": False, "speaking": False}})
                elif msg.get("type") == "ping":
                    await ws.send_text(json.dumps({"type": "pong"}))
        except WebSocketDisconnect:
            connected.discard(ws)

    @app.post("/chat")
    def chat_http(req: ChatRequest):
        if not req.message.strip():
            raise HTTPException(400, "Empty message")
        return {"reply": _process(req.message)}

    @app.get("/health")
    def health():
        return {"status": "ok", "clients": len(connected), "service": "ida-realtime"}

    def run(host: str = "0.0.0.0", port: int = 8765):
        print(f"IDA Realtime Bridge → ws://{host}:{port}/ws")
        uvicorn.run(app, host=host, port=port, log_level="info")

    if __name__ == "__main__":
        run()
else:
    def run(*a, **k):
        print("Install: pip install fastapi uvicorn websockets")
