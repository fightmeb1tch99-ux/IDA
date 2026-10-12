"""
Memory Manager for IDA v5.3 — AIRI-inspired long-term memory
JSON + optional SQLite / vector. Core memory, episode summaries, facts.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

from logger import log_info, log_error, log_debug


class MemoryManager:
    """Manages agent memory with persistence (core + episodic + facts)."""

    MAX_FACTS = 40
    MAX_CORE = 25
    MAX_EPISODES = 30
    SUMMARIZE_EVERY = 8

    def __init__(self, memory_file: str = "memory/memory.json", brain=None):
        self.memory_file = memory_file
        self.backup_dir = Path("memory/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.brain = brain
        self.db = None
        self.vector = None

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
        self._ensure_structure()
        log_info("MemoryManager ready (core + episodic)")

    def _ensure_structure(self) -> None:
        m = self.memory
        defaults = {
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
            "core_memory": [],
            "episodes": [],
            "turns_since_summary": 0,
            "profile": {
                "name": None,
                "city": None,
                "language": "ru",
                "facts": [],
                "summary": "",
            },
        }
        for k, v in defaults.items():
            if k not in m:
                m[k] = v
        if not isinstance(m.get("core_memory"), list):
            m["core_memory"] = []
        if not isinstance(m.get("episodes"), list):
            m["episodes"] = []
        if not isinstance(m.get("facts"), list):
            m["facts"] = []
        if not isinstance(m.get("profile"), dict):
            m["profile"] = defaults["profile"]
        if not m["core_memory"] and m.get("facts"):
            m["core_memory"] = list(m["facts"][: self.MAX_CORE])

    def load(self) -> dict:
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

    def _initialize_memory(self) -> dict:
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
            "core_memory": [],
            "episodes": [],
            "turns_since_summary": 0,
            "profile": {
                "name": None,
                "city": None,
                "language": "ru",
                "facts": [],
                "summary": "",
            },
        }

    def save(self, memory: Optional[dict] = None) -> bool:
        data = memory if memory is not None else self.memory
        data["last_updated"] = datetime.now().isoformat()
        data["interactions_count"] = data.get("interactions_count", 0) + 1

        try:
            if os.path.exists(self.memory_file):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = self.backup_dir / f"memory_{ts}.json"
                shutil.copy2(self.memory_file, backup_path)
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

    def get(self, key: str, default=None):
        return self.memory.get(key, default)

    def set(self, key: str, value: Any):
        self.memory[key] = value
        return value

    def increment_interactions(self) -> int:
        self.memory["interactions_count"] = self.memory.get("interactions_count", 0) + 1
        return self.memory["interactions_count"]

    def get_stats(self) -> dict:
        return {
            "name": self.memory.get("name"),
            "created_at": self.memory.get("created_at"),
            "last_updated": self.memory.get("last_updated"),
            "interactions_count": self.memory.get("interactions_count", 0),
            "core_memory_count": len(self.memory.get("core_memory") or []),
            "episodes_count": len(self.memory.get("episodes") or []),
            "facts_count": len(self.memory.get("facts") or []),
        }

    def _ensure_profile(self) -> dict:
        if "profile" not in self.memory or not isinstance(self.memory.get("profile"), dict):
            self.memory["profile"] = {
                "name": self.memory.get("name"),
                "city": self.memory.get("city"),
                "language": self.memory.get("language") or "ru",
                "facts": list(self.memory.get("facts") or []),
                "summary": self.memory.get("summary") or "",
            }
        prof = self.memory["profile"]
        if self.memory.get("name") and not prof.get("name"):
            prof["name"] = self.memory["name"]
        if self.memory.get("city") and not prof.get("city"):
            prof["city"] = self.memory["city"]
        return prof

    def get_profile(self) -> dict:
        return dict(self._ensure_profile())

    def get_profile_public(self) -> dict:
        p = self._ensure_profile()
        return {
            "name": p.get("name"),
            "city": p.get("city"),
            "language": p.get("language") or "ru",
            "facts_count": len(p.get("facts") or []),
            "core_count": len(self.memory.get("core_memory") or []),
            "summary": (p.get("summary") or self.memory.get("summary") or "")[:200],
        }

    def update_profile(
        self,
        name=None,
        city=None,
        language=None,
        preferences=None,
        facts=None,
        summary=None,
    ) -> dict:
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

    def add_fact(self, fact: str) -> dict:
        if not fact or not str(fact).strip():
            return self.get_profile()
        fact = str(fact).strip()
        prof = self._ensure_profile()
        facts = list(prof.get("facts") or [])
        if fact not in facts:
            facts.append(fact)
            facts = facts[-self.MAX_FACTS :]
            prof["facts"] = facts
            self.memory["facts"] = facts
            self.memory["profile"] = prof
            self.save()
        return self.get_profile()

    def add_core_memory(self, item: str) -> list:
        """Stable long-term facts (AIRI-style core memory)."""
        if not item or not str(item).strip():
            return list(self.memory.get("core_memory") or [])
        item = str(item).strip()
        core = list(self.memory.get("core_memory") or [])
        if item not in core:
            core.append(item)
            core = core[-self.MAX_CORE :]
            self.memory["core_memory"] = core
            self.save()
        return core

    def get_core_memory(self) -> list:
        return list(self.memory.get("core_memory") or [])

    def add_episode(self, summary: str, tags: Optional[list] = None) -> list:
        """Store a compressed episode of conversation."""
        if not summary or not str(summary).strip():
            return list(self.memory.get("episodes") or [])
        ep = {
            "ts": datetime.now().isoformat(),
            "summary": str(summary).strip()[:800],
            "tags": list(tags or [])[:8],
        }
        episodes = list(self.memory.get("episodes") or [])
        episodes.append(ep)
        episodes = episodes[-self.MAX_EPISODES :]
        self.memory["episodes"] = episodes
        self.memory["turns_since_summary"] = 0
        recent = " | ".join(e["summary"][:120] for e in episodes[-3:])
        self.memory["summary"] = recent[:500]
        prof = self._ensure_profile()
        prof["summary"] = self.memory["summary"]
        self.memory["profile"] = prof
        self.save()
        return episodes

    def get_episodes(self, limit: int = 5) -> list:
        eps = list(self.memory.get("episodes") or [])
        return eps[-limit:]

    def note_turn(self) -> int:
        """Call after each user turn; returns turns_since_summary."""
        n = int(self.memory.get("turns_since_summary") or 0) + 1
        self.memory["turns_since_summary"] = n
        return n

    def needs_summary(self) -> bool:
        return int(self.memory.get("turns_since_summary") or 0) >= self.SUMMARIZE_EVERY

    def build_context_block(self) -> str:
        """Text block for system prompt (core + recent episodes + facts)."""
        parts = []
        name = self.memory.get("name") or (self.memory.get("profile") or {}).get("name")
        city = self.memory.get("city") or (self.memory.get("profile") or {}).get("city")
        if name:
            parts.append(f"Имя пользователя: {name}")
        if city:
            parts.append(f"Город: {city}")
        core = self.get_core_memory()
        if core:
            parts.append("Core memory: " + "; ".join(core[-12:]))
        facts = list(self.memory.get("facts") or [])
        if facts:
            parts.append("Факты: " + "; ".join(facts[-8:]))
        eps = self.get_episodes(3)
        if eps:
            parts.append("Недавние эпизоды: " + " || ".join(e["summary"] for e in eps))
        summary = self.memory.get("summary") or ""
        if summary and not eps:
            parts.append(f"Summary: {summary}")
        return "\n".join(parts) if parts else "Профиль пока пуст."
