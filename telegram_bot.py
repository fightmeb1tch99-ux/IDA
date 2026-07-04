"""
IDA Telegram Bot — Mobile Access to your AI Assistant
Allows chatting with IDA, running tools, and setting reminders.
"""

import os
import asyncio
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

from brain import Brain
from memory_manager import MemoryManager
from tools.tools import TOOLS, get_available_tools
from logger import log_info, log_error
from scheduler_manager import scheduler, add_one_time_reminder, setup_morning_brief

# Load environment
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = os.getenv("ALLOWED_USER_IDS", "").split(",")

# Initialize IDA core
memory_mgr = MemoryManager()
memory = memory_mgr.load()
brain = Brain(memory)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    log_info(f"Telegram user started bot: {user.id}")
    
    # Setup morning briefing automatically for the user
    setup_morning_brief(context.application.bot, chat_id, "09:00")
    
    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я IDA — твой проактивный помощник.\n"
        "Теперь я умею ставить напоминания и присылать утренние сводки!\n\n"
        "Попробуй: «Напомни через 5 минут проверить почту»"
    )
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    chat_id = update.effective_chat.id
    
    if ALLOWED_USER_IDS[0] != "" and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ Доступ ограничен.")
        return

    user_text = update.message.text
    log_info(f"TG Message from {user_id}: {user_text}")

    # 1. Decide if a tool is needed
    tool_name, tool_arg = brain.decide_tool(user_text)
    
    tool_result = None
    if tool_name == "remind" and tool_arg:
        # Special handling for reminders
        # tool_arg will be like "5|покормить кота" from brain patterns
        try:
            # Simple parsing for the prompt: "напомни через 5 минут покормить кота"
            # The brain patterns are: (min, text) or (text, min)
            # Let's re-extract here for reliability
            match1 = re.search(r"(?:напомни|напомни\s+мне)\s+(?:через\s+)?(\d+)\s+(?:минут|минуты|мин)\s+(.+)", user_text.lower())
            match2 = re.search(r"(?:напомни|напомни\s+мне)\s+(.+)\s+(?:через\s+)?(\d+)\s+(?:минут|минуты|мин)", user_text.lower())
            
            if match1:
                delay, text = match1.groups()
            elif match2:
                text, delay = match2.groups()
            else:
                delay, text = 5, "что-то важное" # Fallback
            
            tool_result = add_one_time_reminder(context.application.bot, chat_id, text, delay)
        except Exception as e:
            tool_result = f"Ошибка планировщика: {str(e)}"
    
    elif tool_name and tool_name in TOOLS:
        await update.message.reply_chat_action(action="typing")
        try:
            tool_result = TOOLS[tool_name](tool_arg) if tool_arg else TOOLS[tool_name]()
        except Exception as e:
            tool_result = f"Ошибка инструмента: {str(e)}"

    # 2. Generate final response
    response = brain.generate_response(user_text, tool_result)
    
    # 3. Update memory
    brain.add_to_history(user_text, response)
    memory_mgr.save(memory)
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def main():
    if not TELEGRAM_TOKEN:
        print("CRITICAL: TELEGRAM_BOT_TOKEN not found in .env!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start Scheduler
    scheduler.start()
    log_info("Scheduler started.")

    print("🚀 IDA Telegram Bot (v2.3) is starting...")
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # Keep running
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
