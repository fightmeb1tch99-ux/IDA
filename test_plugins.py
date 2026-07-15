"""
Unit tests for the plugin system.
"""
import asyncio
from unittest.mock import patch

import pytest

from plugins.base import BasePlugin
from plugins.manager import PluginManager
from plugins.system.weather import WeatherPlugin


def test_base_plugin_is_abstract():
    with pytest.raises(TypeError):
        BasePlugin("x", "y")


def test_manager_discovers_weather_plugin():
    manager = PluginManager()
    assert "weather" in manager.plugins


def test_manager_plugin_list_has_descriptions():
    manager = PluginManager()
    listing = manager.get_plugin_list()
    assert "weather" in listing
    assert isinstance(listing["weather"], str) and listing["weather"]


def test_execute_unknown_plugin_returns_error():
    manager = PluginManager()
    result = asyncio.run(manager.execute_plugin("nonexistent"))
    assert result["status"] == "error"


def test_weather_plugin_name_and_description():
    plugin = WeatherPlugin()
    assert plugin.name == "Weather"
    assert plugin.description


def test_weather_plugin_handles_network_error():
    plugin = WeatherPlugin()
    with patch("plugins.system.weather.aiohttp.ClientSession", side_effect=Exception("net down")):
        result = asyncio.run(plugin.execute({"city": "Moscow"}))
    assert result["status"] == "error"
    assert "net down" in result["message"]
