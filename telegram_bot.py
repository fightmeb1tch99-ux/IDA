"""
IDA Telegram Bot — Mobile Access to your AI Assistant
Allows chatting with IDA and running tools via Telegram.
"""

import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

from brain import Brain
from memory_manager import MemoryManager
from tools.tools import TOOLS, get_available_tools
from logger import log_info, log_error

# Load environment
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = os.getenv("ALLOWED_USER_IDS", "").split(",") # Security: only you can use it

# Initialize IDA core
memory_mgr = MemoryManager()
memory = memory_mgr.load()
brain = Brain(memory)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    log_info(f"Telegram user started bot: {user.id}")
    
    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я IDA — твой Инновационный Динамический Помощник.\n"
        "Теперь я доступна и в Telegram!\n\n"
        "Напиши мне что-нибудь или используй /help для списка команд."
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a list of available tools."""
    help_text = "🤖 *Команды IDA:*\n\n"
    tools = get_available_tools()
    for name, desc in tools.items():
        help_text += f"• `{name}`: {desc}\n"
    
    help_text += "\nПросто пиши текстом, например: «Какая погода в Москве?»"
    await update.message.reply_markdown(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process user messages through IDA Brain."""
    user_id = str(update.effective_user.id)
    
    # Security Check
    if ALLOWED_USER_IDS[0] != "" and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ Доступ ограничен. Добавьте свой ID в ALLOWED_USER_IDS.")
        return

    user_text = update.message.text
    log_info(f"TG Message from {user_id}: {user_text}")

    # 1. Decide if a tool is needed
    tool_name, tool_arg = brain.decide_tool(user_text)
    
    tool_result = None
    if tool_name and tool_name in TOOLS:
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

def main():
    if not TELEGRAM_TOKEN:
        print("CRITICAL: TELEGRAM_BOT_TOKEN not found in .env!")
        return

    print("🚀 IDA Telegram Bot is starting...")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
