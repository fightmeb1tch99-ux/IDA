"""
IDA API Server — Secure Proxy for Mobile App
Handles OpenAI requests without exposing API keys to the client.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from providers import create_provider

# Load secrets
load_dotenv()
MODEL = os.getenv("IDA_MODEL", "gpt-5-mini")

app = FastAPI(title="IDA API Server")


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7

@app.get("/")
async def root():
    return {"status": "online", "name": "IDA API Server", "version": "1.0"}

@app.post("/v1/chat")
async def chat_proxy(request: ChatRequest):
    """Securely proxy chat requests to the configured LLM provider."""
    provider = create_provider()
    if not provider.is_available():
        raise HTTPException(status_code=500, detail="API Key not configured on server")

    try:
        content = provider.chat(
            [m.model_dump() for m in request.messages],
            model=MODEL,
            temperature=request.temperature,
        )
        return {"response": content}
    except Exception as e:
        print(f"Proxy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
