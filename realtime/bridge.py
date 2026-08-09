"""
IDA Realtime Bridge (sketch)
WebSocket bridge between Python agent and Web Dashboard.

Usage (when ready):
  pip install websockets fastapi uvicorn
  python -m realtime.bridge

This is the foundation for realtime chat + avatar state sync.
"""

from __future__ import annotations
import asyncio
import json
from typing import Set

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False
    print("Install: pip install fastapi uvicorn websockets")

if _AVAILABLE:
    app = FastAPI(title="IDA Realtime Bridge")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    connected: Set[WebSocket] = set()

    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        await ws.accept()
        connected.add(ws)
        try:
            while True:
                data = await ws.receive_text()
                # Broadcast to all clients (simple fan-out)
                msg = {"type": "message", "data": data}
                for client in list(connected):
                    try:
                        await client.send_text(json.dumps(msg))
                    except Exception:
                        connected.discard(client)
        except WebSocketDisconnect:
            connected.discard(ws)

    @app.get("/health")
    def health():
        return {"status": "ok", "clients": len(connected)}

    def run(host: str = "0.0.0.0", port: int = 8765):
        uvicorn.run(app, host=host, port=port)

    if __name__ == "__main__":
        run()
else:
    def run(*args, **kwargs):
        print("Dependencies missing. See requirements.txt")
