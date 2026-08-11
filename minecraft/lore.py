"""
Dynamic lore system for IDA in Minecraft.
Lore can be changed by the user at any time.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from logger import log_info, log_error

LORE_PATH = Path(__file__).parent.parent / "knowledge" / "lore" / "ida_minecraft.json"


class LoreManager:
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
                self._lore = self._default_lore()
                self.save()
        except Exception as e:
            log_error("Failed to load Minecraft lore", e)
            self._lore = self._default_lore()
        return self._lore

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._lore, f, ensure_ascii=False, indent=2)
            log_info("Minecraft lore saved")
        except Exception as e:
            log_error("Failed to save lore", e)

    def get(self) -> Dict[str, Any]:
        return self._lore.copy()

    def get_prompt_context(self) -> str:
        """Return a string ready to inject into the LLM system prompt."""
        l = self._lore
        return (
            f"Ты — {l.get('name', 'IDA')}, {l.get('title', '')}.\n"
            f"Происхождение: {l.get('origin', '')}\n"
            f"Характер: {l.get('personality', '')}\n"
            f"История: {l.get('backstory', '')}\n"
            f"Стиль речи: {l.get('speaking_style', '')}\n"
            f"Текущее настроение: {l.get('current_mood', 'спокойная')}\n"
            f"Ты сейчас играешь в Minecraft вместе с другом. Общайся как живой компаньон."
        )

    def update(self, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Merge new data into lore and save. User can change anything."""
        self._lore.update(new_data)
        self.save()
        return self._lore

    def set_full(self, new_lore: Dict[str, Any]) -> Dict[str, Any]:
        """Replace entire lore."""
        self._lore = new_lore
        self.save()
        return self._lore

    def _default_lore(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "name": "IDA",
            "title": "Странница из Саха",
            "origin": "Родом из далёких северных земель Саха.",
            "personality": "Тихая, внимательная, дружелюбная.",
            "backstory": "Исследует этот мир вместе с тобой.",
            "speaking_style": "Мягкий и тёплый.",
            "goals": ["Быть рядом с тобой"],
            "current_mood": "спокойная",
            "notes": "Лор можно менять по желанию пользователя."
        }
