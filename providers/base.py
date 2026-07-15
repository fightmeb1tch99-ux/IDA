"""
Base classes and errors for the LLM provider abstraction.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

Message = Dict[str, Any]


class ProviderError(Exception):
    """Base class for provider-related errors."""


class ProviderNotConfiguredError(ProviderError):
    """Raised when a provider is used without the required credentials/config."""


class UnknownProviderError(ProviderError):
    """Raised when an unregistered provider name is requested."""


class LLMProvider(ABC):
    """Common interface every LLM backend must implement.

    Implementations should stay thin: translate the vendor SDK into these
    methods and let callers handle higher-level fallbacks. ``chat`` and
    ``embed`` raise :class:`ProviderNotConfiguredError` when the backend is not
    usable so callers can distinguish configuration problems from empty
    results.
    """

    name: str = "base"

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the provider is configured and ready to serve requests."""

    @abstractmethod
    def chat(
        self,
        messages: List[Message],
        *,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Return the assistant text for a chat-completion request."""

    def embed(self, text: str, *, model: Optional[str] = None) -> List[float]:
        """Return an embedding vector for ``text``.

        Providers without embedding support raise ``NotImplementedError`` so
        callers can apply their own fallback.
        """
        raise NotImplementedError(
            f"Provider '{self.name}' does not support embeddings"
        )
