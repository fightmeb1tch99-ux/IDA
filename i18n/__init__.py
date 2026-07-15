"""
Centralized internationalization for IDA OS.

All user-facing prompt/response strings live in :mod:`i18n.prompts` keyed by
language code (``ru``, ``sah``, ``en``). Modules should resolve strings through
:func:`get_prompt` instead of hard-coding text, which keeps translations in one
place and makes adding a language a data-only change.
"""
from i18n.prompts import DEFAULT_LANGUAGE, LANGUAGE_PROMPTS

__all__ = [
    "LANGUAGE_PROMPTS",
    "DEFAULT_LANGUAGE",
    "supported_languages",
    "is_supported",
    "resolve_language",
    "get_prompt",
]


def supported_languages() -> list:
    """Return the list of supported language codes."""
    return list(LANGUAGE_PROMPTS.keys())


def is_supported(language: str) -> bool:
    """Return True if ``language`` has a prompt set."""
    return language in LANGUAGE_PROMPTS


def resolve_language(language: str) -> str:
    """Return ``language`` if supported, otherwise the default language."""
    return language if is_supported(language) else DEFAULT_LANGUAGE


def get_prompt(language: str, key: str, **kwargs) -> str:
    """Return the localized string for ``key``, formatted with ``kwargs``.

    Falls back to the default language when ``language`` is unknown and to an
    empty string when ``key`` is missing.
    """
    prompts = LANGUAGE_PROMPTS.get(language, LANGUAGE_PROMPTS[DEFAULT_LANGUAGE])
    template = prompts.get(key, "")
    return template.format(**kwargs) if kwargs else template
