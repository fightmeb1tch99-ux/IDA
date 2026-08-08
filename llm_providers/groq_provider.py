"""Groq LLM Provider"""

import os
from typing import Optional
from groq import Groq
from .base import BaseLLMProvider, LLMResponse


class GroqProvider(BaseLLMProvider):
    """Groq API Provider - Free and Fast"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "mixtral-8x7b-32768"):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not provided")
        
        super().__init__(api_key, model)
        self.client = Groq(api_key=api_key)
    
    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, **kwargs) -> LLMResponse:
        """Generate response using Groq API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=self.model,
                provider="Groq",
                tokens_used=response.usage.total_tokens,
                success=True
            )
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.model,
                provider="Groq",
                tokens_used=0,
                success=False,
                error=str(e)
            )
    
    def is_available(self) -> bool:
        """Check if Groq API is available"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=10
            )
            return True
        except:
            return False
