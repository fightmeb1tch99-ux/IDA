# IDA Minecraft Companion

IDA может реально зайти на Java Edition сервер и играть с тобой как живой друг.

## Возможности

- Подключение к любому Java-серверу
- Общение в чате
- Следование за игроком
- Динамический лор (можно менять в любой момент)
- Интеграция с мозгом IDA

## Установка

```bash
cd minecraft
npm install
```

Нужен Node.js 18+.

## Быстрый старт

Из Python:

```python
from minecraft import MinecraftBotManager

bot = MinecraftBotManager(brain=your_brain)

# Подключиться
await bot.connect("play.example.com", 25565, username="IDA")

# Сказать что-то в чат
await bot.chat("Привет! Я с тобой~")

# Идти за тобой
await bot.follow_player("YourNick")

# Посмотреть / изменить лор
print(bot.lore.get())
bot.lore.update({"current_mood": "очень радостная", "backstory": "Новая история..."})
```

## Смена лора

Лор лежит в `knowledge/lore/ida_minecraft.json`.  
Можно менять через код или просто попросить IDA:  
«Измени свой лор: теперь ты древний дух леса...»

## Команды бота (через stdin JSON)

- `{"type":"chat","text":"привет"}`
- `{"type":"follow","player":"Nick"}`
- `{"type":"stop"}`
- `{"type":"come","player":"Nick"}`

## Важно

- Только **Java Edition**
- Для online-mode серверов может понадобиться Microsoft-аккаунт (пока offline-режим / cracked)
- Бот работает как отдельный процесс Node.js
