"""
IDA Bot Setup Helper
Quickly configure and start your Telegram bot.
"""

import os

def setup():
    print("🤖 Настройка Telegram-бота IDA")
    token = input("Введите ваш Telegram API Token (от @BotFather): ").strip()
    
    if not token:
        print("❌ Ошибка: Токен не может быть пустым.")
        return

    # Create or update .env file
    env_content = ""
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            env_content = f.read()
    
    if "TELEGRAM_BOT_TOKEN=" in env_content:
        # Update existing token
        lines = env_content.splitlines()
        new_lines = []
        for line in lines:
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                new_lines.append(f"TELEGRAM_BOT_TOKEN={token}")
            else:
                new_lines.append(line)
        env_content = "\n".join(new_lines)
    else:
        # Add new token
        env_content += f"\nTELEGRAM_BOT_TOKEN={token}\n"

    with open(".env", "w") as f:
        f.write(env_content.strip() + "\n")
    
    print("✅ Файл .env обновлен!")
    print("🚀 Запускаю бота...")
    
    # Run the bot
    os.system("python3 telegram_bot.py")

if __name__ == "__main__":
    setup()
