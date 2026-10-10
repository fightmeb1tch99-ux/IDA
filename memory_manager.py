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
            "city": None,
            "language": "ru",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "interactions_count": 0,
            "preferences": {},
            "facts": [],
            "summary": "",
            "custom_data": {},
            "profile": {
                "name": None,
                "city": None,
                "language": "ru",
                "facts": [],
                "summary": "",
            },
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

    def get(self, key, default=None):
        return self.memory.get(key, default)

    def set(self, key, value):
        self.memory[key] = value
        return value

    def increment_interactions(self):
        self.memory["interactions_count"] = self.memory.get("interactions_count", 0) + 1
        return self.memory["interactions_count"]

    def get_stats(self):
        return {
            "name": self.memory.get("name"),
            "created_at": self.memory.get("created_at"),
            "last_updated": self.memory.get("last_updated"),
            "interactions_count": self.memory.get("interactions_count", 0),
        }

    def _ensure_profile(self):
        if "profile" not in self.memory or not isinstance(self.memory.get("profile"), dict):
            self.memory["profile"] = {
                "name": self.memory.get("name"),
                "city": self.memory.get("city"),
                "language": self.memory.get("language") or "ru",
                "facts": list(self.memory.get("facts") or []),
                "summary": self.memory.get("summary") or "",
            }
        # sync top-level convenience fields
        prof = self.memory["profile"]
        if self.memory.get("name") and not prof.get("name"):
            prof["name"] = self.memory["name"]
        if self.memory.get("city") and not prof.get("city"):
            prof["city"] = self.memory["city"]
        return prof

    def get_profile(self):
        return dict(self._ensure_profile())

    def get_profile_public(self):
        p = self._ensure_profile()
        return {
            "name": p.get("name"),
            "city": p.get("city"),
            "language": p.get("language") or "ru",
            "facts_count": len(p.get("facts") or []),
        }

    def update_profile(self, name=None, city=None, language=None, preferences=None, facts=None, summary=None):
        prof = self._ensure_profile()
        if name is not None:
            prof["name"] = name
            self.memory["name"] = name
        if city is not None:
            prof["city"] = city
            self.memory["city"] = city
        if language is not None:
            prof["language"] = language
            self.memory["language"] = language
        if preferences is not None:
            self.memory.setdefault("preferences", {}).update(preferences)
        if facts is not None:
            prof["facts"] = list(facts)
            self.memory["facts"] = list(facts)
        if summary is not None:
            prof["summary"] = summary
            self.memory["summary"] = summary
        self.memory["profile"] = prof
        self.save()
        return self.get_profile()

    def add_fact(self, fact: str):
        if not fact or not str(fact).strip():
            return self.get_profile()
        fact = str(fact).strip()
        prof = self._ensure_profile()
        facts = list(prof.get("facts") or [])
        if fact not in facts:
            facts.append(fact)
            # keep last 30 facts
            facts = facts[-30:]
            prof["facts"] = facts
            self.memory["facts"] = facts
            self.memory["profile"] = prof
            self.save()
        return self.get_profile()
