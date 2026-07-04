"""
Base Agent Class for IDA OS v3.0
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from logger import log_info, log_error

class BaseAgent(ABC):
    def __init__(self, name: str, brain=None):
        self.name = name
        self.brain = brain
        self.history: List[Dict[str, Any]] = []

    @abstractmethod
    async def run(self, task: str, context: str = "") -> Dict[str, Any]:
        pass

    def log(self, message: str):
        log_info(f"[{self.name}] {message}")

    def error(self, message: str, exc: Exception = None):
        log_error(f"[{self.name}] {message}", exc)
