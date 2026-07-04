"""
IDA Scheduler Manager — Background Tasks & Reminders
Handles scheduled notifications and automated briefings.
Fixed for Termux timezone issues.
"""

import os
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from logger import log_info, log_error

# Try to get timezone safely, fallback to UTC if it fails (common in Termux)
try:
    scheduler = AsyncIOScheduler(timezone="UTC")
except Exception as e:
    log_error("Scheduler init error, trying without timezone", e)
    scheduler = AsyncIOScheduler()

async def send_reminder(bot, chat_id, text):
    """Callback function to send a reminder message."""
    try:
        message = f"🔔 *НАПОМИНАНИЕ:* \n\n{text}"
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        log_info(f"Reminder sent to {chat_id}: {text}")
    except Exception as e:
        log_error(f"Failed to send reminder to {chat_id}", e)

def add_one_time_reminder(bot, chat_id, text, delay_minutes):
    """Schedule a one-time reminder."""
    run_time = datetime.now(pytz.utc) + timedelta(minutes=float(delay_minutes))
    scheduler.add_job(
        send_reminder,
        'date',
        run_date=run_time,
        args=[bot, chat_id, text],
        id=f"rem_{chat_id}_{int(run_time.timestamp())}"
    )
    log_info(f"Scheduled reminder for {chat_id} in {delay_minutes} min")
    return f"Ок, бро! Напомню через {delay_minutes} мин: {text}"

async def morning_briefing(bot, chat_id):
    """Daily automated briefing."""
    from tools.tools import TOOLS
    
    weather = TOOLS.get("weather", lambda: "Нет данных")()
    notes = TOOLS.get("note_list", lambda: "Заметок нет")()
    
    briefing = (
        "🌅 *ДОБРОЕ УТРО, БРО!* 🌅\n\n"
        f"🌤 *Погода:* {weather}\n\n"
        f"📝 *Твои заметки:* \n{notes}\n\n"
        "Удачного дня! Я на связи. 🦾"
    )
    try:
        await bot.send_message(chat_id=chat_id, text=briefing, parse_mode="Markdown")
        log_info(f"Morning briefing sent to {chat_id}")
    except Exception as e:
        log_error(f"Failed to send briefing to {chat_id}", e)

def setup_morning_brief(bot, chat_id, time_str="09:00"):
    """Setup daily morning briefing."""
    hour, minute = time_str.split(":")
    try:
        scheduler.add_job(
            morning_briefing,
            CronTrigger(hour=int(hour), minute=int(minute)),
            args=[bot, chat_id],
            id=f"brief_{chat_id}",
            replace_existing=True
        )
        log_info(f"Morning briefing scheduled for {chat_id} at {time_str}")
    except Exception as e:
        log_error("Failed to schedule morning brief", e)
