# IDA Discord Companion

IDA может сидеть в Discord как живой друг: писать в чат, заходить в голосовые каналы, менять свой лор.

## Возможности

- Отвечает на **упоминания** и **личные сообщения**
- Slash-команды: `/ping`, `/lore`, `/join`, `/leave`, `/say`
- Заходит в голосовой канал вместе с тобой
- Динамический **лор** (меняется через `/lore` или просьбу)
- Интеграция с `Brain` и памятью IDA
- Ограничение доступа по `DISCORD_ALLOWED_USER_IDS`

## Установка

```bash
pip install discord.py PyNaCl python-dotenv
```

`PyNaCl` нужен для голосовых каналов.

## Настройка

1. Создай приложение на https://discord.com/developers/applications
2. Bot → Add Bot → скопируй Token
3. Privileged Gateway Intents → включи **MESSAGE CONTENT INTENT**
4. OAuth2 → URL Generator → scopes: `bot`, `applications.commands`
5. Bot Permissions: Send Messages, Connect, Speak, Use Voice Activity
6. Добавь в `.env`:

```env
DISCORD_BOT_TOKEN=твой_токен
DISCORD_OWNER_ID=твой_discord_id
DISCORD_ALLOWED_USER_IDS=id1,id2   # опционально, пусто = все
```

## Запуск

```bash
python -m discord_bot.bot
# или
python discord_bot/bot.py
```

## Команды

| Команда | Описание |
|---------|----------|
| `@IDA привет` | Обычный разговор (через Brain) |
| `/ping` | Проверка онлайна |
| `/lore` | Показать лор |
| `/lore action:set key:backstory value:...` | Изменить лор |
| `/join` | Зайти в твой голосовой канал |
| `/leave` | Выйти из голосового |
| `/say text:...` | Сказать сообщение |

## Лор

Файл: `knowledge/lore/ida_discord.json`  
Можно менять в рантайме — IDA сразу начнёт говорить по-новому.

## Голос (TTS) — следующий шаг

Сейчас бот умеет **заходить** в голосовой канал.  
Чтобы она **говорила** голосом, нужно добавить TTS (edge-tts / piper / ElevenLabs) + FFmpeg.  
Это можно сделать отдельным апдейтом.
