"""
Memory Manager for IDA
JSON memory with optional SQLite / vector (disabled gracefully on Termux).
"""
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from logger import log_info, log_error, log_debug


class MemoryManager:
    """Manages agent memory with persistence."""

    def __init__(self, memory_file="memory/memory.json", brain=None):
        self.memory_file = memory_file
        self.backup_dir = Path("memory/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.brain = brain
        self.db = None
        self.vector = None

        # Optional advanced storage — never crash on Termux
        try:
            from memory.database import DatabaseManager
            self.db = DatabaseManager()
        except Exception as e:
            log_debug(f"SQLite memory disabled: {e}")

        try:
            from memory.vector_storage import VectorStorage
            self.vector = VectorStorage()
        except Exception as e:
            log_debug(f"Vector memory disabled: {e}")

        self.memory = self.load()
        log_info("MemoryManager ready")

    def load(self):
        if not os.path.exists(self.memory_file):
            return self._initialize_memory()
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                memory = json.load(f)
            log_info(f"Memory loaded from {self.memory_file}")
            return memory
        except Exception as e:
            log_error("Failed to load memory", e)
            return self._initialize_memory()

    def _initialize_memory(self):
        return {
            "name": None,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "interactions_count": 0,
            "preferences": {},
            "custom_data": {},
        }

    def save(self, memory=None):
        data = memory if memory is not None else self.memory
        data["last_updated"] = datetime.now().isoformat()
        data["interactions_count"] = data.get("interactions_count", 0) + 1

        try:
            # backup
            if os.path.exists(self.memory_file):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = self.backup_dir / f"memory_{ts}.json"
                shutil.copy2(self.memory_file, backup_path)
                # keep last 10
                backups = sorted(self.backup_dir.glob("memory_*.json"))
                for old in backups[:-10]:
                    try:
                        old.unlink()
                    except Exception:
                        pass

            os.makedirs(os.path.dirname(self.memory_file) or ".", exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.memory = data
            log_debug("Memory saved")
            return True
        except Exception as e:
            log_error("Failed to save memory", e)
            return False
