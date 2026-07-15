"""
Registry and factory for LLM providers.

Backends are registered by name and instantiated on demand. The active
provider defaults to ``config.LLM_PROVIDER`` (env ``IDA_LLM_PROVIDER``) but can
be selected explicitly.
"""
from typing import Callable, Dict, List, Optional

from config import LLM_PROVIDER
from providers.base import LLMProvider, UnknownProviderError
from providers.openai_provider import OllamaProvider, OpenAICompatibleProvider

ProviderBuilder = Callable[..., LLMProvider]

_BUILDERS: Dict[str, ProviderBuilder] = {}


def register_provider(name: str, builder: ProviderBuilder) -> None:
    """Register ``builder`` under ``name`` (case-insensitive)."""
    _BUILDERS[name.lower()] = builder


def available_providers() -> List[str]:
    """Return the sorted list of registered provider names."""
    return sorted(_BUILDERS)


def create_provider(name: Optional[str] = None, **kwargs) -> LLMProvider:
    """Instantiate a provider by name, falling back to the configured default."""
    resolved = (name or LLM_PROVIDER or "openai").lower()
    builder = _BUILDERS.get(resolved)
    if builder is None:
        raise UnknownProviderError(
            f"Unknown LLM provider '{resolved}'. "
            f"Available: {available_providers()}"
        )
    return builder(**kwargs)


register_provider("openai", OpenAICompatibleProvider)
register_provider("openai-compatible", OpenAICompatibleProvider)
register_provider("openrouter", OpenAICompatibleProvider)
register_provider("ollama", OllamaProvider)
