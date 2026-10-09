"""
IDA API Server — Secure Proxy for Mobile App
Handles LLM requests without exposing API keys to the client.
"""

import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL = os.getenv("IDA_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    print("CRITICAL: OPENAI_API_KEY not found in environment!")

try:
    import openai
    client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE) if OPENAI_API_KEY else None
except ImportError:
    client = None

app = FastAPI(title="IDA API Server")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7


@app.get("/")
async def root():
    return {"status": "online", "name": "IDA API Server", "version": "4.1"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ida-api",
        "llm_configured": bool(OPENAI_API_KEY and client),
    }


@app.post("/v1/chat")
async def chat_proxy(request: ChatRequest):
    if not OPENAI_API_KEY or not client:
        raise HTTPException(status_code=500, detail="API Key not configured on server")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[m.model_dump() for m in request.messages],
            temperature=request.temperature,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print(f"Proxy error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail="Upstream LLM request failed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
