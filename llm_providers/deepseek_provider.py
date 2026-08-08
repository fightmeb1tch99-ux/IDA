"""DeepSeek LLM Provider"""

import os
from typing import Optional
import requests
from .base import BaseLLMProvider, LLMResponse


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek API Provider - Free and Powerful"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat"):
        api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not provided")
        
        super().__init__(api_key, model)
        self.base_url = "https://api.deepseek.com/v1"
    
    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, **kwargs) -> LLMResponse:
        """Generate response using DeepSeek API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return LLMResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=self.model,
                    provider="DeepSeek",
                    tokens_used=data.get("usage", {}).get("total_tokens", 0),
                    success=True
                )
            else:
                return LLMResponse(
                    content="",
                    model=self.model,
                    provider="DeepSeek",
                    tokens_used=0,
                    success=False,
                    error=f"API Error: {response.status_code}"
                )
        except Exception as e:
            return LLMResponse(
                content="",
                model=self.model,
                provider="DeepSeek",
                tokens_used=0,
                success=False,
                error=str(e)
            )
    
    def is_available(self) -> bool:
        """Check if DeepSeek API is available"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "ping"}],
                    "max_tokens": 10
                },
                headers=headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
