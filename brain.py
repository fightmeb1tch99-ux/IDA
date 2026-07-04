"""
Brain module for IDA OS v3.0
Enhanced with Reasoning, ReAct support, and Multilingual capabilities.
"""
import re
import os
import json
from logger import log_info, log_error, log_debug, log_warning
from config import (
    LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS,
    OPENAI_API_KEY, OPENAI_API_BASE, CONTEXT_WINDOW,
    EMBEDDING_MODEL
)

# Multilingual support: Russian, Sakha (Yakut), English
LANGUAGE_PROMPTS = {
    'ru': {
        'system': "Ты — IDA OS, автономный ИИ-агент. Твоя задача — помогать пользователю. Отвечай на русском языке.",
        'thought': "Ты — IDA OS. Проанализируй задачу шаг за шагом и напиши краткий план действий.\nЗадача: {input}",
        'tool_decision': "System: Identify if any tool is needed for this task: '{input}'. Available tools: weather, calculator, search, stats. Respond ONLY in JSON format: {{\"tool\": \"tool_name\" or null, \"arg\": \"argument\" or null}}",
        'api_error': "OpenAI API key missing.",
        'llm_error': "Ошибка при генерации ответа: {error}",
        'empty_response': "Я выполнил задачу, но не смог сформулировать текстовый ответ. Система работает в штатном режиме.",
        'news_fallback': "Я нашел новости, но не смог их кратко пересказать. Пожалуйста, проверь результаты поиска напрямую.",
    },
    'sah': {
        'system': "Эн — IDA OS, автономнай ИИ-агент. Эн сабай — аат туох кыттыы. Саха тылынан хоруй.",
        'thought': "Эн — IDA OS. Ыйыы сокуоннарын анализ кыл эбэтэр сокуон плана бичи.\nЫйыы: {input}",
        'tool_decision': "System: Identify if any tool is needed for this task: '{input}'. Available tools: weather, calculator, search, stats. Respond ONLY in JSON format: {{\"tool\": \"tool_name\" or null, \"arg\": \"argument\" or null}}",
        'api_error': "OpenAI API ачкы сокуобалаа.",
        'llm_error': "Хоруу уонна сыаналлаах алгыс: {error}",
        'empty_response': "Мин ыйыыны ылыппын, онно эмэ тиэкиэл хоруу сыаналлаах алгыс сыаналлаа алдьатпын.",
        'news_fallback': "Мин сэргэ сыаналлаа сыаналлаа алдьатпын, онно эмэ сокуоннарын кыскаанан сыаналлаа алдьатпын.",
    },
    'en': {
        'system': "You are IDA OS, an autonomous AI agent. Your task is to help the user. Respond in English.",
        'thought': "You are IDA OS. Analyze the task step by step and write a brief action plan.\nTask: {input}",
        'tool_decision': "System: Identify if any tool is needed for this task: '{input}'. Available tools: weather, calculator, search, stats. Respond ONLY in JSON format: {{\"tool\": \"tool_name\" or null, \"arg\": \"argument\" or null}}",
        'api_error': "OpenAI API key missing.",
        'llm_error': "Error generating response: {error}",
        'empty_response': "I completed the task, but couldn't formulate a text response. The system is operating normally.",
        'news_fallback': "I found news, but couldn't summarize them briefly. Please check the search results directly.",
    }
}

class Brain:
    def __init__(self, memory: dict):
        self.memory = memory
        self.conversation_history = []
        self.client = None
        self.language = memory.get('language', 'ru')  # Default to Russian
    
    def set_language(self, language: str):
        """Set the language for responses. Supported: 'ru', 'sah', 'en'"""
        if language in LANGUAGE_PROMPTS:
            self.language = language
            log_info(f"Language set to: {language}")
        else:
            log_warning(f"Language '{language}' not supported. Using Russian.")
            self.language = 'ru'
    
    def _get_prompt(self, key: str, **kwargs) -> str:
        """Get localized prompt string"""
        prompts = LANGUAGE_PROMPTS.get(self.language, LANGUAGE_PROMPTS['ru'])
        template = prompts.get(key, '')
        return template.format(**kwargs) if kwargs else template

    def _get_client(self):
        if self.client is None:
            try:
                from openai import OpenAI
                api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
                api_base = OPENAI_API_BASE or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
                if api_key:
                    self.client = OpenAI(api_key=api_key, base_url=api_base)
            except Exception as e:
                log_error("Failed to init OpenAI client", e)
        return self.client

    def generate_thought(self, user_input: str) -> str:
        """Generate a reasoning chain before acting."""
        prompt = self._get_prompt('thought', input=user_input)
        return self._get_llm_response(prompt, temperature=0.2)

    def generate_response(self, user_input: str, tool_result=None, thought=None) -> str:
        client = self._get_client()
        if not client:
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
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                temperature=LLM_TEMPERATURE,
                max_tokens=LLM_MAX_TOKENS
            )
            if response and response.choices:
                content = response.choices[0].message.content
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
        client = self._get_client()
        if not client: return ""
        try:
            log_debug(f"LLM Request Prompt: {prompt[:100]}...")
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            if response and response.choices:
                content = response.choices[0].message.content
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
        client = self._get_client()
        if not client: return []
        try:
            response = client.embeddings.create(
                input=text,
                model=EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            # Fallback: Return a pseudo-random embedding based on text hash if API fails
            log_warning(f"Embeddings API not available. Using fallback mechanism.")
            import hashlib
            hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            pseudo_vec = [(hash_val >> i) & 1 for i in range(1536)]
            return [float(x) for x in pseudo_vec]

    def decide_tool(self, user_input: str) -> tuple:
        """Decide which tool to use and extract arguments."""
        prompt = self._get_prompt('tool_decision', input=user_input)
        response = self._get_llm_response(prompt, temperature=0)
        try:
            import json
            data = json.loads(response)
            return data.get("tool"), data.get("arg")
        except:
            return None, None

    def add_to_history(self, user: str, response: str):
        self.conversation_history.append({"user": user, "response": response})
