"""
Unit tests for AI Agent components.

Run with: python3 -m pytest test_agent.py -v
Or: python3 test_agent.py
"""

import unittest
import json
import os
import tempfile
import shutil
from pathlib import Path

# Import components to test
from brain import CommandParser, Brain
from memory_manager import MemoryManager
from tools.tools import (
    get_time, get_date, create_file, run_command, web_search,
    get_available_tools
)


class TestCommandParser(unittest.TestCase):
    """Test the command parser."""
    
    def setUp(self):
        self.parser = CommandParser()
    
    def test_time_commands(self):
        """Test time command variations."""
        test_cases = [
            ("какое время", "time"),
            ("которое время", "time"),
            ("текущее время", "time"),
            ("сколько времени", "time"),
        ]
        
        for text, expected_tool in test_cases:
            tool_name, _ = self.parser.parse(text)
            self.assertEqual(tool_name, expected_tool, f"Failed for: {text}")
    
    def test_date_commands(self):
        """Test date command variations."""
        test_cases = [
            ("какая дата", "date"),
            ("текущая дата", "date"),
            ("сегодня", "date"),
            ("какое число", "date"),
        ]
        
        for text, expected_tool in test_cases:
            tool_name, _ = self.parser.parse(text)
            self.assertEqual(tool_name, expected_tool, f"Failed for: {text}")
    
    def test_file_creation_commands(self):
        """Test file creation command variations."""
        test_cases = [
            ("создай файл test.txt", "create_file"),
            ("создать файл data.json", "create_file"),
            ("новый файл document.md", "create_file"),
        ]
        
        for text, expected_tool in test_cases:
            tool_name, arg = self.parser.parse(text)
            self.assertEqual(tool_name, expected_tool, f"Failed for: {text}")
            self.assertIsNotNone(arg, f"No argument extracted for: {text}")
    
    def test_search_commands(self):
        """Test search command variations."""
        test_cases = [
            ("найди информацию о Python", "search"),
            ("поиск машинного обучения", "search"),
            ("ищи новости", "search"),
            ("гугли погода", "search"),
        ]
        
        for text, expected_tool in test_cases:
            tool_name, arg = self.parser.parse(text)
            self.assertEqual(tool_name, expected_tool, f"Failed for: {text}")
            self.assertIsNotNone(arg, f"No argument extracted for: {text}")
    
    def test_help_commands(self):
        """Test help command variations."""
        test_cases = [
            ("помощь", "help"),
            ("помоги", "help"),
            ("что ты умеешь", "help"),
            ("команды", "help"),
        ]
        
        for text, expected_tool in test_cases:
            tool_name, _ = self.parser.parse(text)
            self.assertEqual(tool_name, expected_tool, f"Failed for: {text}")
    
    def test_invalid_commands(self):
        """Test that invalid commands return None."""
        test_cases = [
            "случайный текст",
            "абракадабра",
            "фыва",
        ]
        
        for text in test_cases:
            tool_name, _ = self.parser.parse(text)
            self.assertIsNone(tool_name, f"Should not match: {text}")


class TestBrain(unittest.TestCase):
    """Test the Brain class."""
    
    def setUp(self):
        self.memory = {"name": "TestUser"}
        self.brain = Brain(self.memory)
    
    def test_greeting_response(self):
        """Test greeting responses."""
        response = self.brain.generate_response("привет")
        self.assertIsNotNone(response)
        self.assertIn("👋", response)
    
    def test_name_saving(self):
        """Test name saving functionality."""
        response = self.brain.generate_response("меня зовут Иван")
        self.assertIn("Иван", response)
        self.assertEqual(self.memory["name"], "Иван")
    
    def test_name_retrieval(self):
        """Test name retrieval."""
        self.memory["name"] = "Петр"
        response = self.brain.generate_response("как меня зовут")
        self.assertIn("Петр", response)
    
    def test_help_message(self):
        """Test help message generation."""
        response = self.brain.generate_response("помощь")
        self.assertIn("Доступные команды", response)
        self.assertIn("Время", response)
    
    def test_conversation_history(self):
        """Test conversation history tracking."""
        self.brain.add_to_history("привет", "Йо 👋")
        history = self.brain.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["user"], "привет")


class TestMemoryManager(unittest.TestCase):
    """Test the MemoryManager class."""
    
    def setUp(self):
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.memory_file = os.path.join(self.test_dir, "test_memory.json")
    
    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_memory_initialization(self):
        """Test memory initialization."""
        manager = MemoryManager(self.memory_file)
        self.assertIsNotNone(manager.memory)
        self.assertIn("name", manager.memory)
        self.assertIn("created_at", manager.memory)
    
    def test_memory_save_and_load(self):
        """Test saving and loading memory."""
        manager = MemoryManager(self.memory_file)
        manager.set("name", "TestUser")
        manager.save()
        
        # Load in new instance
        manager2 = MemoryManager(self.memory_file)
        self.assertEqual(manager2.get("name"), "TestUser")
    
    def test_memory_increment(self):
        """Test interaction counter."""
        manager = MemoryManager(self.memory_file)
        initial = manager.get("interactions_count", 0)
        manager.increment_interactions()
        self.assertEqual(manager.get("interactions_count"), initial + 1)
    
    def test_memory_stats(self):
        """Test statistics retrieval."""
        manager = MemoryManager(self.memory_file)
        manager.set("name", "TestUser")
        stats = manager.get_stats()
        
        self.assertIn("name", stats)
        self.assertIn("created_at", stats)
        self.assertIn("interactions_count", stats)


class TestTools(unittest.TestCase):
    """Test the tools module."""
    
    def test_get_time(self):
        """Test time tool."""
        result = get_time()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{2}:\d{2}:\d{2}")
    
    def test_get_date(self):
        """Test date tool."""
        result = get_date()
        self.assertIsNotNone(result)
        self.assertRegex(result, r"\d{4}-\d{2}-\d{2}")
    
    def test_create_file_valid(self):
        """Test file creation with valid filename."""
        # Use temporary directory
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
        """Test file creation with invalid path (security test)."""
        result = create_file("../../../etc/passwd")
        self.assertIn("недопустимый путь", result)
    
    def test_create_file_invalid_input(self):
        """Test file creation with invalid input."""
        result = create_file("")
        self.assertIn("некорректное имя", result)
        
        result = create_file(None)
        self.assertIn("некорректное имя", result)
    
    def test_run_command_safe(self):
        """Test running a safe command."""
        result = run_command("echo hello")
        self.assertIn("hello", result)
    
    def test_run_command_unsafe(self):
        """Test that unsafe commands are blocked."""
        result = run_command("rm -rf /")
        self.assertIn("не разрешена", result)
    
    def test_run_command_invalid_input(self):
        """Test running command with invalid input."""
        result = run_command("")
        self.assertIn("некорректная команда", result)
    
    def test_get_available_tools(self):
        """Test getting available tools list."""
        tools = get_available_tools()
        self.assertIn("time", tools)
        self.assertIn("date", tools)
        self.assertIn("create_file", tools)
        self.assertIn("run", tools)
        self.assertIn("search", tools)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.memory_file = os.path.join(self.test_dir, "test_memory.json")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_full_workflow(self):
        """Test a complete workflow."""
        # Initialize components
        memory_manager = MemoryManager(self.memory_file)
        brain = Brain(memory_manager.memory)
        
        # Simulate user interaction
        parser = CommandParser()
        
        # Test 1: Greeting
        tool_name, _ = parser.parse("привет")
        self.assertIsNone(tool_name)  # No tool needed
        response = brain.generate_response("привет")
        self.assertIn("👋", response)
        
        # Test 2: Name saving
        response = brain.generate_response("меня зовут Мария")
        self.assertIn("Мария", response)
        memory_manager.save()
        
        # Test 3: Name retrieval
        response = brain.generate_response("как меня зовут")
        self.assertIn("Мария", response)
        
        # Test 4: Help
        response = brain.generate_response("помощь")
        self.assertIn("Доступные команды", response)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCommandParser))
    suite.addTests(loader.loadTestsFromTestCase(TestBrain))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryManager))
    suite.addTests(loader.loadTestsFromTestCase(TestTools))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
