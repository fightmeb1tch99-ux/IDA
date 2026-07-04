"""
IDA Telegram Bot — Optimized for Fast Start
Uses lazy loading for heavy modules like Vision, RAG, and Scheduler.
"""

import os
import asyncio
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

# Essential imports only
from memory_manager import MemoryManager
from brain import Brain
from tools.tools import TOOLS
from logger import log_info, log_error

# Load environment
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = os.getenv("ALLOWED_USER_IDS", "").split(",")

# Initialize IDA core (Fast)
memory_mgr = MemoryManager()
memory = memory_mgr.load()
brain = Brain(memory)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    log_info(f"Telegram user started bot: {user.id}")
    
    # Lazy load scheduler for morning brief
    from scheduler_manager import setup_morning_brief
    setup_morning_brief(context.application.bot, chat_id, "09:00")
    
    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я IDA — твой оптимизированный помощник.\n"
        "Теперь я запускаюсь быстрее! ⚡\n\n"
        "📸 Пришли мне фото или напиши «Нарисуй...»"
    )
    await update.message.reply_text(welcome_text)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photos with lazy-loaded Vision module."""
    user_id = str(update.effective_user.id)
    if ALLOWED_USER_IDS[0] != "" and user_id not in ALLOWED_USER_IDS:
        return

    await update.message.reply_chat_action(action="typing")
    
    # Lazy load Vision
    from vision_art import analyze_image
    
    photo_file = await update.message.photo[-1].get_file()
    file_path = f"downloads/{photo_file.file_id}.jpg"
    os.makedirs("downloads", exist_ok=True)
    await photo_file.download_to_drive(file_path)
    
    caption = update.message.caption if update.message.caption else "Что на этом фото?"
    analysis = analyze_image(file_path, caption)
    
    await update.message.reply_text(f"👁️ *Анализ фото:* \n\n{analysis}", parse_mode="Markdown")
    os.remove(file_path)

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
    if tool_name == "draw" and tool_arg:
        # Lazy load Image Gen
        from vision_art import generate_image
        await update.message.reply_text("🎨 Рисую для тебя, подожди немного...")
        await update.message.reply_chat_action(action="upload_photo")
        image_url = generate_image(tool_arg)
        if image_url.startswith("http"):
            await update.message.reply_photo(photo=image_url, caption=f"Вот твой арт по запросу: {tool_arg}")
            return
        else:
            tool_result = image_url

    elif tool_name == "remind" and tool_arg:
        # Lazy load Scheduler
        from scheduler_manager import add_one_time_reminder
        match1 = re.search(r"(?:напомни|напомни\s+мне)\s+(?:через\s+)?(\d+)\s+(?:минут|минуты|мин)\s+(.+)", user_text.lower())
        match2 = re.search(r"(?:напомни|напомни\s+мне)\s+(.+)\s+(?:через\s+)?(\d+)\s+(?:минут|минуты|мин)", user_text.lower())
        if match1: delay, text = match1.groups()
        elif match2: text, delay = match2.groups()
        else: delay, text = 5, "что-то важное"
        tool_result = add_one_time_reminder(context.application.bot, chat_id, text, delay)
    
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
    memory_mgr.save()
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def main():
    if not TELEGRAM_TOKEN:
        print("CRITICAL: TELEGRAM_BOT_TOKEN not found in .env!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start Scheduler in background
    from scheduler_manager import scheduler
    scheduler.start()
    
    print("🚀 IDA Telegram Bot (v2.5 Optimized) is starting...")
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        while True: await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
