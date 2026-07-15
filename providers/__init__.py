"""
LLM provider abstraction for IDA OS.

The rest of the codebase talks to language models through the small
:class:`~providers.base.LLMProvider` interface instead of importing a vendor
SDK directly. Any OpenAI-compatible backend (OpenAI, Ollama, OpenRouter,
vLLM, local proxies) is served by :class:`OpenAICompatibleProvider`; a new
vendor only needs to implement :class:`LLMProvider` and register a builder.

Typical use::

    from providers import create_provider

    provider = create_provider()          # picks backend from config
    text = provider.chat([{"role": "user", "content": "Hi"}])
"""
from providers.base import (
    LLMProvider,
    ProviderError,
    ProviderNotConfiguredError,
    UnknownProviderError,
)
from providers.openai_provider import OllamaProvider, OpenAICompatibleProvider
from providers.registry import (
    available_providers,
    create_provider,
    register_provider,
)

__all__ = [
    "LLMProvider",
    "ProviderError",
    "ProviderNotConfiguredError",
    "UnknownProviderError",
    "OpenAICompatibleProvider",
    "OllamaProvider",
    "create_provider",
    "register_provider",
    "available_providers",
]
