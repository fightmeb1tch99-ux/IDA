"""
Unit tests for the LLM provider abstraction.
"""
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from providers import (
    LLMProvider,
    OllamaProvider,
    OpenAICompatibleProvider,
    ProviderNotConfiguredError,
    UnknownProviderError,
    available_providers,
    create_provider,
    register_provider,
)


def _chat_response(content):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


class TestRegistry:
    def test_default_provider_is_openai(self):
        provider = create_provider()
        assert isinstance(provider, OpenAICompatibleProvider)
        assert provider.name == "openai"

    def test_named_provider_ollama(self):
        provider = create_provider("ollama")
        assert isinstance(provider, OllamaProvider)

    def test_name_is_case_insensitive(self):
        assert isinstance(create_provider("OpenAI"), OpenAICompatibleProvider)

    def test_unknown_provider_raises(self):
        with pytest.raises(UnknownProviderError):
            create_provider("does-not-exist")

    def test_available_providers_lists_builtins(self):
        names = available_providers()
        assert "openai" in names
        assert "ollama" in names

    def test_register_custom_provider(self):
        class DummyProvider(LLMProvider):
            name = "dummy"

            def is_available(self):
                return True

            def chat(self, messages, *, model=None, temperature=None, max_tokens=None):
                return "dummy"

        register_provider("dummy-test", DummyProvider)
        assert isinstance(create_provider("dummy-test"), DummyProvider)


class TestOpenAICompatibleProvider:
    def test_not_available_without_key(self):
        provider = OpenAICompatibleProvider(api_key="")
        assert provider.is_available() is False

    def test_chat_without_key_raises(self):
        provider = OpenAICompatibleProvider(api_key="")
        with pytest.raises(ProviderNotConfiguredError):
            provider.chat([{"role": "user", "content": "hi"}])

    def test_embed_without_key_raises(self):
        provider = OpenAICompatibleProvider(api_key="")
        with pytest.raises(ProviderNotConfiguredError):
            provider.embed("hi")

    def test_chat_returns_stripped_content(self):
        with patch("openai.OpenAI") as mock_openai:
            client = mock_openai.return_value
            client.chat.completions.create.return_value = _chat_response("  hello  ")
            provider = OpenAICompatibleProvider(api_key="key")
            assert provider.is_available() is True
            assert provider.chat([{"role": "user", "content": "hi"}]) == "hello"

    def test_chat_empty_choices_returns_empty(self):
        with patch("openai.OpenAI") as mock_openai:
            client = mock_openai.return_value
            client.chat.completions.create.return_value = SimpleNamespace(choices=[])
            provider = OpenAICompatibleProvider(api_key="key")
            assert provider.chat([{"role": "user", "content": "hi"}]) == ""

    def test_chat_passes_model_and_params(self):
        with patch("openai.OpenAI") as mock_openai:
            client = mock_openai.return_value
            client.chat.completions.create.return_value = _chat_response("ok")
            provider = OpenAICompatibleProvider(api_key="key")
            provider.chat(
                [{"role": "user", "content": "hi"}],
                model="custom-model",
                temperature=0.1,
                max_tokens=42,
            )
            _, kwargs = client.chat.completions.create.call_args
            assert kwargs["model"] == "custom-model"
            assert kwargs["temperature"] == 0.1
            assert kwargs["max_tokens"] == 42

    def test_embed_returns_vector(self):
        with patch("openai.OpenAI") as mock_openai:
            client = mock_openai.return_value
            client.embeddings.create.return_value = SimpleNamespace(
                data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3])]
            )
            provider = OpenAICompatibleProvider(api_key="key")
            assert provider.embed("text") == [0.1, 0.2, 0.3]


class TestOllamaProvider:
    def test_defaults(self):
        provider = OllamaProvider()
        assert provider.api_key == "ollama"
        assert provider.api_base == "http://localhost:11434/v1"

    def test_openai_base_env_does_not_override_localhost(self, monkeypatch):
        # A globally configured OpenAI endpoint must not hijack local Ollama.
        monkeypatch.setenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        provider = OllamaProvider()
        assert provider.api_base == "http://localhost:11434/v1"

    def test_explicit_ollama_base_env_is_respected(self, monkeypatch):
        monkeypatch.setenv("OLLAMA_API_BASE", "http://gpu-box:11434/v1")
        provider = OllamaProvider()
        assert provider.api_base == "http://gpu-box:11434/v1"
