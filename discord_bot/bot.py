"""
IDA Discord Bot — text chat, voice join, lore, Brain integration.
"""

import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from logger import log_info, log_error
from .lore import DiscordLoreManager

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ALLOWED_USER_IDS = [x.strip() for x in os.getenv("DISCORD_ALLOWED_USER_IDS", "").split(",") if x.strip()]
OWNER_ID = os.getenv("DISCORD_OWNER_ID", "")

# Lazy brain import to keep startup fast
_brain = None
_memory = None


def get_brain():
    global _brain, _memory
    if _brain is None:
        from memory_manager import MemoryManager
        from brain import Brain
        _memory = MemoryManager().load()
        _brain = Brain(_memory)
    return _brain


lore = DiscordLoreManager()


class IDABot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.guilds = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync slash commands to guilds (faster than global)
        await self.tree.sync()
        log_info("Discord slash commands synced")


bot = IDABot()


def is_allowed(user_id: int) -> bool:
    if not ALLOWED_USER_IDS:
        return True
    return str(user_id) in ALLOWED_USER_IDS or str(user_id) == OWNER_ID


@bot.event
async def on_ready():
    log_info(f"IDA Discord online as {bot.user} (id={bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="тебя ❤️")
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if not is_allowed(message.author.id):
        return

    # Only respond when mentioned or in DM
    is_dm = isinstance(message.channel, discord.DMChannel)
    mentioned = bot.user and bot.user.mentioned_in(message)

    if not (is_dm or mentioned):
        await bot.process_commands(message)
        return

    content = message.content
    if bot.user:
        content = content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

    if not content:
        await message.reply("Да, я здесь~ Напиши, что нужно.")
        return

    async with message.channel.typing():
        try:
            brain = get_brain()
            # Inject lore into context
            system_extra = lore.get_system_prompt()
            # Use existing brain — most brains accept a message string
            if hasattr(brain, "think"):
                reply = await asyncio.to_thread(brain.think, content, system_extra)
            elif hasattr(brain, "chat"):
                reply = await asyncio.to_thread(brain.chat, content)
            elif hasattr(brain, "generate"):
                reply = await asyncio.to_thread(brain.generate, content)
            else:
                # Fallback: simple response using decide_tool style if available
                reply = f"Я тебя услышала: «{content}». (Подключи Brain.think для полных ответов)"

            if not reply:
                reply = "..."

            # Discord limit 2000 chars
            if len(reply) > 1900:
                reply = reply[:1900] + "…"

            await message.reply(reply)
        except Exception as e:
            log_error("Discord message handler error", e)
            await message.reply("Что-то пошло не так... Попробуй ещё раз.")

    await bot.process_commands(message)


# ---------- Slash commands ----------

@bot.tree.command(name="ping", description="Проверка, что IDA онлайн")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message("Понг~ Я здесь ❤️", ephemeral=True)


@bot.tree.command(name="lore", description="Показать или изменить лор IDA")
@app_commands.describe(action="show | set", key="поле лора (personality, backstory...)", value="новое значение")
async def slash_lore(
    interaction: discord.Interaction,
    action: str = "show",
    key: str = None,
    value: str = None,
):
    if not is_allowed(interaction.user.id):
        await interaction.response.send_message("Нет доступа.", ephemeral=True)
        return

    if action == "show" or not key:
        data = lore.get()
        text = "\n".join(f"**{k}**: {v}" for k, v in data.items() if k != "notes")
        await interaction.response.send_message(f"**Лор IDA:**\n{text}", ephemeral=True)
        return

    if action == "set" and key and value:
        lore.update({key: value})
        await interaction.response.send_message(f"Обновила `{key}` → {value}", ephemeral=True)
        return

    await interaction.response.send_message("Использование: `/lore action:set key:backstory value:Новая история`", ephemeral=True)


@bot.tree.command(name="join", description="Зайти в голосовой канал")
async def slash_join(interaction: discord.Interaction):
    if not is_allowed(interaction.user.id):
        await interaction.response.send_message("Нет доступа.", ephemeral=True)
        return

    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("Сначала зайди в голосовой канал.", ephemeral=True)
        return

    channel = interaction.user.voice.channel
    voice = interaction.guild.voice_client

    if voice and voice.channel == channel:
        await interaction.response.send_message("Я уже здесь~", ephemeral=True)
        return

    if voice:
        await voice.move_to(channel)
    else:
        await channel.connect()

    await interaction.response.send_message(f"Зашла в **{channel.name}** 🎤")


@bot.tree.command(name="leave", description="Выйти из голосового канала")
async def slash_leave(interaction: discord.Interaction):
    if not is_allowed(interaction.user.id):
        await interaction.response.send_message("Нет доступа.", ephemeral=True)
        return

    voice = interaction.guild.voice_client
    if voice:
        await voice.disconnect()
        await interaction.response.send_message("Вышла из голосового.")
    else:
        await interaction.response.send_message("Я не в голосовом канале.", ephemeral=True)


@bot.tree.command(name="say", description="Сказать что-то от имени IDA в текущий канал")
@app_commands.describe(text="Текст сообщения")
async def slash_say(interaction: discord.Interaction, text: str):
    if not is_allowed(interaction.user.id):
        await interaction.response.send_message("Нет доступа.", ephemeral=True)
        return
    await interaction.response.send_message(text)


def run_discord_bot():
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_BOT_TOKEN не задан в .env")
    log_info("Starting IDA Discord bot...")
    bot.run(DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    run_discord_bot()
