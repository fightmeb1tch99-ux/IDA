"""
Base Plugin Class for IDA OS v3.0
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlugin(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        pass
