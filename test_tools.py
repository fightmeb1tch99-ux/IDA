"""
Unit tests for the tools module (calculator, notes, weather, search).
"""
from pathlib import Path
from unittest.mock import patch

import pytest

import tools.tools as tools_module
from tools.tools import (
    add_note,
    calculate,
    get_weather,
    list_notes,
    web_search,
)


class TestCalculator:
    def test_basic_arithmetic(self):
        assert calculate("2 + 2") == "2 + 2 = 4"

    def test_empty_expression(self):
        assert "пустое" in calculate("")

    def test_division_by_zero(self):
        assert "деление на ноль" in calculate("1/0")

    def test_strips_unsafe_characters(self):
        # letters/symbols are removed, leaving a valid numeric expression
        assert calculate("2+2abc").endswith("= 4")

    def test_only_unsafe_characters(self):
        assert "недопустимые символы" in calculate("abc")


class TestNotes:
    @pytest.fixture(autouse=True)
    def temp_notes(self, tmp_path):
        with patch.object(tools_module, "NOTES_FILE", Path(tmp_path) / "notes.json"):
            yield

    def test_list_when_empty(self):
        assert "Заметок пока нет" in list_notes()

    def test_add_and_list_note(self):
        assert "сохранена" in add_note("buy milk")
        listing = list_notes()
        assert "buy milk" in listing

    def test_add_empty_note_rejected(self):
        assert "пустая" in add_note("")


class TestWeather:
    def test_handles_network_error(self):
        with patch("tools.tools.urllib.request.urlopen", side_effect=Exception("boom")):
            result = get_weather("Yakutsk")
        assert "Не удалось получить погоду" in result


class TestWebSearch:
    def test_empty_query(self):
        assert "пустой запрос" in web_search("")

    def test_handles_generic_error(self):
        with patch("tools.tools.urllib.request.urlopen", side_effect=Exception("boom")):
            result = web_search("python")
        assert "Ошибка поиска" in result
