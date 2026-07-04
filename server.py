"""
IDA API Server — Secure Proxy for Mobile App
Handles OpenAI requests without exposing API keys to the client.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import openai
from dotenv import load_dotenv

# Load secrets
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL = os.getenv("IDA_MODEL", "gpt-5-mini")

if not OPENAI_API_KEY:
    print("CRITICAL: OPENAI_API_KEY not found in environment!")

app = FastAPI(title="IDA API Server")
client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

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
    """Securely proxy chat requests to OpenAI."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured on server")
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[m.model_dump() for m in request.messages],
            temperature=request.temperature
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        print(f"Proxy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
