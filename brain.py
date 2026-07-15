"""
Brain module for IDA OS v3.0
Enhanced with Reasoning, ReAct support, and Multilingual capabilities.
"""
import json
from logger import log_info, log_error, log_debug, log_warning
from config import LLM_TEMPERATURE, CONTEXT_WINDOW
from i18n import DEFAULT_LANGUAGE, LANGUAGE_PROMPTS, get_prompt, is_supported
from providers import create_provider

# Re-exported for backward compatibility; the source of truth is i18n.prompts.
__all__ = ["Brain", "LANGUAGE_PROMPTS"]


class Brain:
    def __init__(self, memory: dict):
        self.memory = memory
        self.conversation_history = []
        self.provider = None
        self.language = memory.get('language', DEFAULT_LANGUAGE)
    
    def set_language(self, language: str):
        """Set the language for responses. Supported: 'ru', 'sah', 'en'"""
        if is_supported(language):
            self.language = language
            log_info(f"Language set to: {language}")
        else:
            log_warning(f"Language '{language}' not supported. Using Russian.")
            self.language = DEFAULT_LANGUAGE
    
    def _get_prompt(self, key: str, **kwargs) -> str:
        """Get localized prompt string"""
        return get_prompt(self.language, key, **kwargs)

    def _get_provider(self):
        """Lazily create the configured LLM provider."""
        if self.provider is None:
            self.provider = create_provider()
        return self.provider

    def generate_thought(self, user_input: str) -> str:
        """Generate a reasoning chain before acting."""
        prompt = self._get_prompt('thought', input=user_input)
        return self._get_llm_response(prompt, temperature=0.2)

    def generate_response(self, user_input: str, tool_result=None, thought=None) -> str:
        provider = self._get_provider()
        if not provider.is_available():
            return self._get_prompt('api_error')
            
        system_prompt = self._get_prompt('system')
        if thought and isinstance(thought, str) and thought.strip():
            system_prompt += f"\nТвой внутренний анализ: {thought}"
            
        messages = [{"role": "system", "content": system_prompt}]
        
        # Safe history access
        history = self.conversation_history or []
        for entry in history[-CONTEXT_WINDOW:]:
            if entry.get("user") and entry.get("response"):
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["response"]})
            
        if tool_result:
            messages.append({"role": "system", "content": f"Данные от инструментов: {tool_result}"})
            
        messages.append({"role": "user", "content": user_input})
        
        try:
            content = provider.chat(messages, temperature=LLM_TEMPERATURE)
            if content and content.strip():
                return content.strip()
            
            # If empty, try a simpler prompt
            log_warning("LLM returned empty response, retrying with simple prompt...")
            simple_resp = self._get_llm_response(f"Answer the user's question: {user_input}")
            if simple_resp and simple_resp.strip():
                return simple_resp
            
            # Final fallback for OS stability
            if "новости" in user_input.lower() or "news" in user_input.lower():
                return self._get_prompt('news_fallback')
            return self._get_prompt('empty_response')
            
        except Exception as e:
            log_error("LLM Generation failed", e)
            return self._get_prompt('llm_error', error=str(e))

    def _get_llm_response(self, prompt: str, temperature=0.7) -> str:
        provider = self._get_provider()
        if not provider.is_available():
            return ""
        try:
            log_debug(f"LLM Request Prompt: {prompt[:100]}...")
            content = provider.chat(
                [{"role": "user", "content": prompt}], temperature=temperature
            )
            if content:
                log_debug(f"LLM Response: {content[:100]}...")
                return content.strip()
            log_warning("LLM returned empty choices or content")
            return ""
        except Exception as e:
            log_error("LLM Call failed", e)
            return ""

    def get_embedding(self, text: str) -> list:
        """Generate embedding for a given text."""
        provider = self._get_provider()
        if not provider.is_available():
            return []
        try:
            return provider.embed(text)
        except Exception:
            # Fallback: Return a pseudo-random embedding based on text hash if API fails
            log_warning("Embeddings API not available. Using fallback mechanism.")
            import hashlib
            hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            pseudo_vec = [(hash_val >> i) & 1 for i in range(1536)]
            return [float(x) for x in pseudo_vec]

    def decide_tool(self, user_input: str) -> tuple:
        """Decide which tool to use and extract arguments."""
        prompt = self._get_prompt('tool_decision', input=user_input)
        response = self._get_llm_response(prompt, temperature=0)
        try:
            data = json.loads(response)
            return data.get("tool"), data.get("arg")
        except Exception:
            return None, None

    def add_to_history(self, user: str, response: str):
        self.conversation_history.append({"user": user, "response": response})
