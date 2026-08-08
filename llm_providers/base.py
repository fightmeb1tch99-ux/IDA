"""Base LLM Provider Interface"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standard LLM response format"""
    content: str
    model: str
    provider: str
    tokens_used: int
    success: bool
    error: Optional[str] = None


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.provider_name = self.__class__.__name__
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate response from LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            "provider": self.provider_name,
            "model": self.model,
            "available": self.is_available()
        }
