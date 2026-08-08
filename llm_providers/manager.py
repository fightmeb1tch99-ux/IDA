"""LLM Provider Manager - Routes requests to best available provider"""

import os
from typing import List, Optional, Dict, Any
from .base import BaseLLMProvider, LLMResponse
from .groq_provider import GroqProvider
from .deepseek_provider import DeepSeekProvider


class LLMManager:
    """Manages multiple LLM providers with fallback"""
    
    def __init__(self):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.priority_order: List[str] = []
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize all available providers"""
        # Groq (Primary - fastest and most reliable)
        if os.getenv("GROQ_API_KEY"):
            try:
                self.providers["groq"] = GroqProvider()
                self.priority_order.append("groq")
            except:
                pass
        
        # DeepSeek (Secondary - powerful alternative)
        if os.getenv("DEEPSEEK_API_KEY"):
            try:
                self.providers["deepseek"] = DeepSeekProvider()
                self.priority_order.append("deepseek")
            except:
                pass
        
        if not self.providers:
            raise ValueError("No LLM providers configured")
    
    def generate(self, prompt: str, provider: Optional[str] = None, **kwargs) -> LLMResponse:
        """Generate response with fallback"""
        # If specific provider requested
        if provider and provider in self.providers:
            response = self.providers[provider].generate(prompt, **kwargs)
            if response.success:
                return response
        
        # Try providers in priority order
        for provider_name in self.priority_order:
            provider = self.providers[provider_name]
            response = provider.generate(prompt, **kwargs)
            if response.success:
                return response
        
        # All providers failed
        return LLMResponse(
            content="",
            model="unknown",
            provider="none",
            tokens_used=0,
            success=False,
            error="All LLM providers failed"
        )
    
    def get_best_provider(self, task_type: str = "general") -> Optional[str]:
        """Get best provider for specific task type"""
        task_routing = {
            "code": "groq",  # Groq is best for code
            "reasoning": "deepseek",  # DeepSeek is good for reasoning
            "general": "groq",  # Groq is fastest
            "translation": "deepseek",
            "summarization": "groq"
        }
        
        provider = task_routing.get(task_type, "groq")
        if provider in self.providers:
            return provider
        
        # Fallback to first available
        return self.priority_order[0] if self.priority_order else None
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {
            "total_providers": len(self.providers),
            "available_providers": [],
            "providers": {}
        }
        
        for name, provider in self.providers.items():
            is_available = provider.is_available()
            status["providers"][name] = {
                "available": is_available,
                "model": provider.model,
                "config": provider.get_config()
            }
            if is_available:
                status["available_providers"].append(name)
        
        return status
    
    def list_providers(self) -> List[str]:
        """List all configured providers"""
        return list(self.providers.keys())
