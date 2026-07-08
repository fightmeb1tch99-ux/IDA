"""
Groq API Client for IDA
Инновационный динамический помощник
Создатель: Григорьев Айтал Григорьевич (@Mareioak)
"""

import os
from typing import Optional
from logger import log_info, log_error, log_debug

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    log_error("Groq library not installed. Install with: pip install groq")


class GroqClient:
    """Groq API client for IDA"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client"""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            log_error("GROQ_API_KEY not found in environment variables")
            self.client = None
            return
        
        if not GROQ_AVAILABLE:
            log_error("Groq library not installed")
            self.client = None
            return
        
        try:
            self.client = Groq(api_key=self.api_key)
            log_info("Groq client initialized successfully")
        except Exception as e:
            log_error(f"Failed to initialize Groq client: {e}")
            self.client = None
    
    def chat(self, message: str, model: str = "mixtral-8x7b-32768", 
             temperature: float = 0.7, max_tokens: int = 1024) -> Optional[str]:
        """
        Send a message to Groq and get a response
        
        Args:
            message: User message
            model: Groq model to use
            temperature: Response creativity (0-2)
            max_tokens: Maximum response length
        
        Returns:
            Response text or None if error
        """
        if not self.client:
            log_error("Groq client not initialized")
            return None
        
        try:
            log_debug(f"Sending message to Groq: {message[:80]}")
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            result = response.choices[0].message.content
            log_info(f"Groq response received ({len(result)} chars)")
            return result
        
        except Exception as e:
            log_error(f"Groq API error: {e}")
            return None
    
    def chat_with_history(self, messages: list, model: str = "mixtral-8x7b-32768",
                         temperature: float = 0.7, max_tokens: int = 1024) -> Optional[str]:
        """
        Send messages with history to Groq
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Groq model to use
            temperature: Response creativity
            max_tokens: Maximum response length
        
        Returns:
            Response text or None if error
        """
        if not self.client:
            log_error("Groq client not initialized")
            return None
        
        try:
            log_debug(f"Sending {len(messages)} messages to Groq")
            
            response = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            result = response.choices[0].message.content
            log_info(f"Groq response received ({len(result)} chars)")
            return result
        
        except Exception as e:
            log_error(f"Groq API error: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Groq client is available"""
        return self.client is not None


# Global Groq client instance
_groq_client = None


def get_groq_client() -> Optional[GroqClient]:
    """Get or create global Groq client"""
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient()
    return _groq_client


def groq_chat(message: str) -> Optional[str]:
    """Convenience function for Groq chat"""
    client = get_groq_client()
    if client and client.is_available():
        return client.chat(message)
    return None
