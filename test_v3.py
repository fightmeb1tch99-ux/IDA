"""
Smoke tests for IDA core (v5.2).
"""
from pathlib import Path
from brain import Brain
from memory_manager import MemoryManager


def test_memory_manager_loads():
    mm = MemoryManager()
    mem = mm.load()
    assert isinstance(mem, dict)


def test_profile_update():
    mm = MemoryManager(memory_file="memory/test_profile_tmp.json")
    mm.update_profile(name="TestUser", city="Yakutsk")
    p = mm.get_profile()
    assert p["name"] == "TestUser"
    assert p["city"] == "Yakutsk"
    pub = mm.get_profile_public()
    assert pub["name"] == "TestUser"


def test_brain_profile_from_text():
    brain = Brain({})
    brain.maybe_update_profile("Меня зовут Айтал")
    assert brain.memory.get("name") == "Айтал"


def test_brain_without_api_key():
    brain = Brain({})
    assert brain is not None
    tool, _ = brain.decide_tool("какое время")
    assert tool == "time"


def test_main_version_string():
    main_text = Path("main.py").read_text(encoding="utf-8")
    assert "v5.1" in main_text or "v5.2" in main_text


def test_api_server_exists():
    assert Path("api_server.py").exists()
    text = Path("api_server.py").read_text(encoding="utf-8")
    assert "/api/chat" in text
    assert "/ws" in text
    assert "/api/profile" in text


def test_health_endpoint_exists():
    server_text = Path("api_server.py").read_text(encoding="utf-8")
    assert "/health" in server_text
