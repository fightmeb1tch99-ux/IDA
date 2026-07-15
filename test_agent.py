"""
Unit tests for AI Agent components.

Run with: python3 -m pytest test_agent.py -v
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch

from brain import Brain
from memory_manager import MemoryManager
from tools.tools import (
    create_file,
    get_available_tools,
    get_date,
    get_time,
    run_command,
)


class TestBrain(unittest.TestCase):
    """Test the Brain class (LLM access is mocked)."""

    def setUp(self):
        self.brain = Brain({"language": "ru", "name": "TestUser"})

    def _fake_provider(self, reply):
        provider = Mock()
        provider.is_available.return_value = True
        provider.chat.return_value = reply
        return provider

    def test_generate_response_returns_llm_content(self):
        with patch.object(self.brain, "_get_provider", return_value=self._fake_provider("Привет 👋")):
            response = self.brain.generate_response("привет")
        self.assertEqual(response, "Привет 👋")

    def test_generate_response_without_provider(self):
        provider = Mock()
        provider.is_available.return_value = False
        with patch.object(self.brain, "_get_provider", return_value=provider):
            response = self.brain.generate_response("привет")
        self.assertEqual(response, self.brain._get_prompt("api_error"))

    def test_conversation_history(self):
        self.brain.add_to_history("привет", "Йо 👋")
        history = self.brain.conversation_history
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user"], "привет")


class TestMemoryManager(unittest.TestCase):
    """Test the MemoryManager class."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.memory_file = os.path.join(self.test_dir, "test_memory.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_memory_initialization(self):
        manager = MemoryManager(self.memory_file)
        self.assertIsNotNone(manager.memory)
        self.assertIn("name", manager.memory)
        self.assertIn("created_at", manager.memory)

    def test_memory_save_and_load(self):
        manager = MemoryManager(self.memory_file)
        manager.set("name", "TestUser")
        manager.save()

        manager2 = MemoryManager(self.memory_file)
        self.assertEqual(manager2.get("name"), "TestUser")

    def test_memory_increment(self):
        manager = MemoryManager(self.memory_file)
        initial = manager.get("interactions_count", 0)
        manager.increment_interactions()
        self.assertEqual(manager.get("interactions_count"), initial + 1)

    def test_memory_stats(self):
        manager = MemoryManager(self.memory_file)
        manager.set("name", "TestUser")
        self.assertEqual(manager.get("name"), "TestUser")
        self.assertIn("created_at", manager.memory)
        self.assertIn("interactions_count", manager.memory)


class TestTools(unittest.TestCase):
    """Test the tools module."""

    def test_get_time(self):
        result = get_time()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{2}:\d{2}:\d{2}")

    def test_get_date(self):
        result = get_date()
        self.assertIsNotNone(result)
        self.assertIn("2026", result)

    def test_create_file_valid(self):
        test_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        try:
            os.chdir(test_dir)
            result = create_file("test.txt")
            self.assertIn("создан", result)
            self.assertTrue(os.path.exists("created_files/test.txt"))
        finally:
            os.chdir(original_cwd)
            shutil.rmtree(test_dir, ignore_errors=True)

    def test_create_file_invalid_path(self):
        result = create_file("../../../etc/passwd")
        self.assertIn("недопустимый путь", result)

    def test_create_file_invalid_input(self):
        self.assertIn("некорректное имя", create_file(""))
        self.assertIn("некорректное имя", create_file(None))

    def test_run_command_safe(self):
        result = run_command("echo hello")
        self.assertIn("hello", result)

    def test_run_command_unsafe(self):
        result = run_command("rm -rf /")
        self.assertIn("не разрешена", result)

    def test_run_command_invalid_input(self):
        self.assertIn("некорректная команда", run_command(""))

    def test_get_available_tools(self):
        tools = get_available_tools()
        self.assertIn("time", tools)
        self.assertIn("date", tools)
        self.assertIn("create_file", tools)
        self.assertIn("run", tools)
        self.assertIn("search", tools)


if __name__ == "__main__":
    unittest.main(verbosity=2)
