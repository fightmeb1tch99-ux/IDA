"""
Plugin Manager for IDA OS v3.0
Handles discovery and execution of plugins.
"""
import os
import importlib
from typing import Dict, Any
from logger import log_info, log_error
from plugins.base import BasePlugin

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self._load_plugins()

    def _load_plugins(self):
        # Load system plugins
        system_plugins_path = "plugins/system"
        if os.path.exists(system_plugins_path):
            for file in os.listdir(system_plugins_path):
                if file.endswith(".py") and not file.startswith("__"):
                    module_name = f"plugins.system.{file[:-3]}"
                    try:
                        module = importlib.import_module(module_name)
                        # Find classes that inherit from BasePlugin
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr is not BasePlugin:
                                plugin_instance = attr()
                                self.plugins[plugin_instance.name.lower()] = plugin_instance
                                log_info(f"Loaded plugin: {plugin_instance.name}")
                    except Exception as e:
                        log_error(f"Failed to load plugin {module_name}", e)

    async def execute_plugin(self, name: str, args: Dict[str, Any] = None):
        name = name.lower()
        if name in self.plugins:
            return await self.plugins[name].execute(args)
        return {"status": "error", "message": f"Plugin {name} not found"}

    def get_plugin_list(self):
        return {name: p.description for name, p in self.plugins.items()}
