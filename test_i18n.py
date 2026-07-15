"""
Unit tests for the centralized i18n module.
"""
from i18n import (
    DEFAULT_LANGUAGE,
    LANGUAGE_PROMPTS,
    get_prompt,
    is_supported,
    resolve_language,
    supported_languages,
)

REQUIRED_KEYS = {
    "system",
    "thought",
    "tool_decision",
    "api_error",
    "llm_error",
    "empty_response",
    "news_fallback",
}


def test_supported_languages():
    langs = supported_languages()
    assert "ru" in langs
    assert "en" in langs
    assert "sah" in langs


def test_is_supported():
    assert is_supported("ru") is True
    assert is_supported("xx") is False


def test_resolve_language_falls_back_to_default():
    assert resolve_language("en") == "en"
    assert resolve_language("unknown") == DEFAULT_LANGUAGE


def test_get_prompt_returns_localized_text():
    assert "IDA OS" in get_prompt("ru", "system")
    assert "English" in get_prompt("en", "system")


def test_get_prompt_formats_kwargs():
    prompt = get_prompt("en", "thought", input="do X")
    assert "do X" in prompt


def test_get_prompt_unknown_language_uses_default():
    assert get_prompt("xx", "system") == get_prompt(DEFAULT_LANGUAGE, "system")


def test_get_prompt_missing_key_returns_empty():
    assert get_prompt("ru", "nonexistent_key") == ""


def test_all_languages_have_required_keys():
    for lang, prompts in LANGUAGE_PROMPTS.items():
        assert set(prompts.keys()) == REQUIRED_KEYS, f"Language '{lang}' key mismatch"


def test_all_prompts_are_non_empty_strings():
    for lang, prompts in LANGUAGE_PROMPTS.items():
        for key, value in prompts.items():
            assert isinstance(value, str) and value, f"{lang}/{key} empty"
