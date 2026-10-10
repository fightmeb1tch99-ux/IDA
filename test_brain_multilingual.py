"""
Unit tests for Brain module (current API).
"""
import pytest
from brain import Brain, CommandParser


class TestCommandParser:
    def test_parse_time(self):
        parser = CommandParser()
        tool, arg = parser.parse("Какое сейчас время?")
        assert tool == "time"

    def test_parse_help(self):
        parser = CommandParser()
        tool, arg = parser.parse("помощь")
        assert tool == "help"

    def test_parse_calc(self):
        parser = CommandParser()
        tool, arg = parser.parse("посчитай 2 + 2")
        assert tool == "calc"
        assert arg is not None


class TestBrain:
    @pytest.fixture
    def brain(self):
        return Brain({"language": "ru"})

    def test_init(self, brain):
        assert brain.memory.get("language") == "ru"
        assert brain.conversation_history == []
        assert brain.parser is not None

    def test_decide_tool_time(self, brain):
        tool, arg = brain.decide_tool("который час")
        assert tool == "time"

    def test_help_message(self, brain):
        msg = brain._get_help_message()
        assert "время" in msg.lower() or "команд" in msg.lower()

    def test_generate_response_help(self, brain):
        resp = brain.generate_response("помощь")
        assert isinstance(resp, str)
        assert len(resp) > 10

    def test_add_to_history(self, brain):
        brain.add_to_history("привет", "здарова")
        hist = brain.get_history()
        assert len(hist) >= 1
