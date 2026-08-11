"""
IDA Minecraft Companion Module
Allows IDA to join a Java Edition server as a real playable friend.
"""

from .bot_manager import MinecraftBotManager
from .lore import LoreManager

__all__ = ["MinecraftBotManager", "LoreManager"]
