"""
Smoke tests for IDA main entry and core modules.
"""
from pathlib import Path
from brain import Brain
from memory_manager import MemoryManager


def test_memory_manager_loads():
    mm = MemoryManager()
    mem = mm.load()
    assert isinstance(mem, dict)


def test_brain_without_api_key():
    brain = Brain({})
    assert brain is not None
    tool, _ = brain.decide_tool("какое время")
    assert tool == "time"


def test_main_version_string():
    main_text = Path("main.py").read_text(encoding="utf-8")
    assert "v5.1" in main_text


def test_health_endpoint_exists():
    server_text = Path("server.py").read_text(encoding="utf-8")
    assert "/health" in server_text
