"""
IDA Discord Companion
Text + Voice channel support, dynamic lore, Brain integration.
"""

from .bot import run_discord_bot
from .lore import DiscordLoreManager

__all__ = ["run_discord_bot", "DiscordLoreManager"]
