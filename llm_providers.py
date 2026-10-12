"""
IDA LLM Providers — unified multi-provider layer (AIRI-inspired).
Supports: Groq, OpenAI-compatible, Ollama, OpenRouter.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from logger import log_info, log_error, log_warning, log_debug


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str


class BaseProvider:
    name = "base"

    def is_available(self) -> bool:
        return False

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: Optional[str] = None,
    ) -> LLMResponse:
        raise NotImplementedError


class GroqProvider(BaseProvider):
    name = "groq"

    def __init__(self):
        self.client = None
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        key = (os.getenv("GROQ_API_KEY") or "").strip()
        if not key or not key.startswith("gsk_"):
            return
        try:
            from groq import Groq
            self.client = Groq(api_key=key)
            log_info(f"LLM provider ready: groq ({self.model})")
        except Exception as e:
            log_debug(f"Groq unavailable: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def chat(self, messages, temperature=0.7, max_tokens=1024, model=None) -> LLMResponse:
        m = model or self.model
        r = self.client.chat.completions.create(
            model=m,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = (r.choices[0].message.content or "").strip()
        return LLMResponse(content=text, provider=self.name, model=m)


class OpenAICompatibleProvider(BaseProvider):
    """OpenAI official + any OpenAI-compatible (OpenRouter, local proxies, etc.)."""

    name = "openai"

    def __init__(
        self,
        name: str = "openai",
        api_key_env: str = "OPENAI_API_KEY",
        base_url_env: str = "OPENAI_API_BASE",
        default_base: str = "https://api.openai.com/v1",
        default_model: str = "gpt-4o-mini",
        model_env: str = "IDA_MODEL",
    ):
        self.name = name
        self.client = None
        self.model = os.getenv(model_env) or os.getenv("OPENAI_MODEL") or default_model
        key = (os.getenv(api_key_env) or "").strip()
        base = (os.getenv(base_url_env) or default_base).strip()
        bad = {"", "sk-...", "sk-proj-...", "your_key_here", "вставь"}
        if not key or key in bad or len(key) < 12:
            return
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=key, base_url=base)
            log_info(f"LLM provider ready: {self.name} ({self.model} @ {base})")
        except Exception as e:
            log_debug(f"{self.name} unavailable: {e}")

    def is_available(self) -> bool:
        return self.client is not None

    def chat(self, messages, temperature=0.7, max_tokens=1024, model=None) -> LLMResponse:
        m = model or self.model
        r = self.client.chat.completions.create(
            model=m,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = (r.choices[0].message.content or "").strip()
        return LLMResponse(content=text, provider=self.name, model=m)


class OllamaProvider(BaseProvider):
    name = "ollama"

    def __init__(self):
        self.base = (os.getenv("OLLAMA_BASE_URL") or "http://127.0.0.1:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL") or os.getenv("IDA_MODEL") or "llama3.2"
        self._ok = False
        try:
            import urllib.request
            req = urllib.request.Request(f"{self.base}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    self._ok = True
                    log_info(f"LLM provider ready: ollama ({self.model} @ {self.base})")
        except Exception as e:
            log_debug(f"Ollama unavailable: {e}")

    def is_available(self) -> bool:
        return self._ok

    def chat(self, messages, temperature=0.7, max_tokens=1024, model=None) -> LLMResponse:
        import json
        import urllib.request

        m = model or self.model
        # Convert to Ollama chat format
        payload = {
            "model": m,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        text = (body.get("message") or {}).get("content") or body.get("response") or ""
        return LLMResponse(content=str(text).strip(), provider=self.name, model=m)


class LLMRouter:
    """
    Priority (AIRI-style config override via IDA_LLM_PROVIDER):
      env IDA_LLM_PROVIDER=groq|openai|ollama|openrouter
      else: groq → openrouter → openai → ollama
    """

    def __init__(self):
        self.providers: list[BaseProvider] = []
        preferred = (os.getenv("IDA_LLM_PROVIDER") or "").strip().lower()

        groq = GroqProvider()
        openrouter = OpenAICompatibleProvider(
            name="openrouter",
            api_key_env="OPENROUTER_API_KEY",
            base_url_env="OPENROUTER_BASE_URL",
            default_base="https://openrouter.ai/api/v1",
            default_model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            model_env="OPENROUTER_MODEL",
        )
        openai_p = OpenAICompatibleProvider(
            name="openai",
            api_key_env="OPENAI_API_KEY",
            base_url_env="OPENAI_API_BASE",
            default_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            default_model=os.getenv("IDA_MODEL", "gpt-4o-mini"),
            model_env="IDA_MODEL",
        )
        ollama = OllamaProvider()

        by_name = {
            "groq": groq,
            "openrouter": openrouter,
            "openai": openai_p,
            "ollama": ollama,
        }

        ordered: list[BaseProvider] = []
        if preferred in by_name:
            ordered.append(by_name[preferred])
        for p in (groq, openrouter, openai_p, ollama):
            if p not in ordered:
                ordered.append(p)

        self.providers = [p for p in ordered if p.is_available()]
        if self.providers:
            names = ", ".join(f"{p.name}" for p in self.providers)
            log_info(f"LLM router active: [{names}] (primary={self.providers[0].name})")
        else:
            log_warning(
                "Нет рабочего LLM. Добавь GROQ_API_KEY / OPENAI_API_KEY / "
                "OPENROUTER_API_KEY или запусти Ollama. "
                "Groq бесплатно: https://console.groq.com/keys"
            )

    def is_available(self) -> bool:
        return bool(self.providers)

    @property
    def primary_name(self) -> str:
        return self.providers[0].name if self.providers else "none"

    def chat(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        model: Optional[str] = None,
    ) -> LLMResponse:
        last_err: Optional[Exception] = None
        for p in self.providers:
            try:
                return p.chat(messages, temperature=temperature, max_tokens=max_tokens, model=model)
            except Exception as e:
                last_err = e
                log_error(f"LLM {p.name} failed, trying next", e)
        if last_err:
            raise last_err
        raise RuntimeError("No LLM providers available")


_router: Optional[LLMRouter] = None


def get_router() -> LLMRouter:
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
