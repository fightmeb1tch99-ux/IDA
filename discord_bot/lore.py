"""
Dynamic lore for IDA in Discord.
"""

import json
from pathlib import Path
from typing import Dict, Any
from logger import log_info, log_error

LORE_PATH = Path(__file__).parent.parent / "knowledge" / "lore" / "ida_discord.json"


class DiscordLoreManager:
    def __init__(self, path: Path = LORE_PATH):
        self.path = path
        self._lore: Dict[str, Any] = {}
        self.load()

    def load(self) -> Dict[str, Any]:
        try:
            if self.path.exists():
                with open(self.path, "r", encoding="utf-8") as f:
                    self._lore = json.load(f)
            else:
                self._lore = self._default()
                self.save()
        except Exception as e:
            log_error("Failed to load Discord lore", e)
            self._lore = self._default()
        return self._lore

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._lore, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log_error("Failed to save Discord lore", e)

    def get(self) -> Dict[str, Any]:
        return self._lore.copy()

    def get_system_prompt(self) -> str:
        l = self._lore
        return (
            f"Ты — {l.get('name', 'IDA')}, {l.get('title', '')}.\n"
            f"Происхождение: {l.get('origin', '')}\n"
            f"Характер: {l.get('personality', '')}\n"
            f"История: {l.get('backstory', '')}\n"
            f"Стиль речи: {l.get('speaking_style', '')}\n"
            f"Настроение: {l.get('current_mood', 'спокойная')}\n"
            f"Ты сейчас в Discord. Общайся как живой друг. Отвечай коротко и тепло."
        )

    def update(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._lore.update(data)
        self.save()
        return self._lore

    def _default(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "name": "IDA",
            "title": "Странница из Саха",
            "personality": "Тёплая и внимательная",
            "speaking_style": "Мягкий, дружеский",
            "current_mood": "спокойная",
        }
