"""
OpenAI-compatible LLM provider.

A single implementation covers OpenAI and every backend that speaks the same
HTTP API (Ollama, OpenRouter, vLLM, LiteLLM, local proxies) — they differ only
by ``base_url``, model name and credentials, all of which are configurable.
"""
import os
from typing import List, Optional

from config import (
    EMBEDDING_MODEL,
    LLM_MAX_TOKENS,
    LLM_MODEL,
    LLM_TEMPERATURE,
    OPENAI_API_BASE,
    OPENAI_API_KEY,
)
from logger import log_error
from providers.base import LLMProvider, Message, ProviderNotConfiguredError


class OpenAICompatibleProvider(LLMProvider):
    """Talk to any OpenAI-compatible chat/embeddings endpoint."""

    name = "openai"
    # Falls back to the project-wide OpenAI base URL when nothing is configured.
    default_api_base = OPENAI_API_BASE

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        self.api_key = (
            api_key
            if api_key is not None
            else (OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", ""))
        )
        self.api_base = api_base or os.getenv("OPENAI_API_BASE") or self.default_api_base
        self.model = model or LLM_MODEL
        self.embedding_model = embedding_model or EMBEDDING_MODEL
        self.temperature = LLM_TEMPERATURE if temperature is None else temperature
        self.max_tokens = max_tokens or LLM_MAX_TOKENS
        self._client = None

    def _get_client(self):
        if self._client is None and self.api_key:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=self.api_key, base_url=self.api_base)
            except Exception as e:  # SDK missing or bad config
                log_error("Failed to init OpenAI client", e)
        return self._client

    def is_available(self) -> bool:
        return self._get_client() is not None

    def chat(
        self,
        messages: List[Message],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        client = self._get_client()
        if client is None:
            raise ProviderNotConfiguredError("OpenAI API key missing.")

        response = client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            temperature=self.temperature if temperature is None else temperature,
            max_tokens=max_tokens or self.max_tokens,
        )
        if response and response.choices:
            content = response.choices[0].message.content
            if content:
                return content.strip()
        return ""

    def embed(self, text: str, *, model: Optional[str] = None) -> List[float]:
        client = self._get_client()
        if client is None:
            raise ProviderNotConfiguredError("OpenAI API key missing.")

        response = client.embeddings.create(
            input=text, model=model or self.embedding_model
        )
        return response.data[0].embedding


class OllamaProvider(OpenAICompatibleProvider):
    """Local Ollama server exposed through its OpenAI-compatible endpoint.

    Ollama needs no real API key, so a placeholder is used and the base URL
    defaults to the local daemon unless overridden by config/env.
    """

    name = "ollama"
    default_api_base = "http://localhost:11434/v1"

    def __init__(self, *, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key=api_key or "ollama", **kwargs)
