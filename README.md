```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   ██╗██████╗  █████╗                                           ║
║   ██║██╔══██╗██╔══██╗                                          ║
║   ██║██║  ██║███████║                                          ║
║   ██║██║  ██║██╔══██║                                          ║
║   ██║██████╔╝██║  ██║                                          ║
║   ╚═╝╚═════╝ ╚═╝  ╚═╝                                          ║
║                                                                ║
║     Инновационный Динамический Помощник  •  v5.1               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

# IDA — Инновационный Динамический AI-помощник

**IDA** — полноценная экосистема персонального ИИ-помощника с живым аватаром, голосом, памятью и возможностью **реально играть с тобой в Minecraft**.

Работает в терминале (Termux / ПК), веб-браузере, мобильном приложении и как компаньон в Minecraft.

**Автор:** Айтал Григорьев ([@fightmeb1tch99-ux](https://github.com/fightmeb1tch99-ux))

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![Expo](https://img.shields.io/badge/Expo-Mobile-000020?logo=expo)](https://expo.dev)
[![Live2D](https://img.shields.io/badge/Live2D-Avatar-ff69b4)](https://www.live2d.com/)
[![Minecraft](https://img.shields.io/badge/Minecraft-Companion-green)](https://www.minecraft.net/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-v5.1-success)](https://github.com/fightmeb1tch99-ux/IDA)

---

## ✨ Возможности v5.0

### 🧠 Интеллект
- **Multi-LLM** — OpenAI, Groq, Claude, Gemini, Mistral и другие
- Долгосрочная память + RAG
- Понимание команд на **русском, якутском и английском**
- Динамический **лор** — личность IDA можно менять в любой момент

### 👤 Живой аватар (Live2D)
- Полноценная поддержка Live2D Cubism
- Компонент `Live2DAvatar` (React)
- Оптимизация памяти и GPU для всех устройств (ПК + телефон)
- Адаптивный размер, touch-события, ограничение FPS
- Scaffold готов в `client/public/live2d/ida/` и `avatar/live2d/`
- Описание персонажа: `avatar/ida-live2d-character.json`


### 💬 Discord-компаньон
- Отвечает на упоминания и ЛС
- Заходит в голосовые каналы (`/join`, `/leave`)
- Динамический лор (`/lore`)
- Интеграция с Brain
- Модуль: `discord_bot/`

### 🎮 Minecraft-компаньон
- IDA **реально заходит** на Java Edition сервер и играет с тобой
- Общается в чате как живой друг
- Может следовать за тобой, останавливаться, приходить
- Имеет свой **лор**, который меняется по твоей просьбе
- Модуль: `minecraft/` (Mineflayer + Python manager)

### 🛠️ Инструменты
| Команда | Описание |
|---------|----------|
| Время / Дата | Текущее время и дата |
| Погода | Прогноз через wttr.in |
| Калькулятор | Безопасные вычисления |
| Заметки | Сохранение и поиск заметок |
| Поиск | DuckDuckGo |
| Файлы | Безопасное создание файлов |
| Системные команды | Whitelist безопасных команд |
| Голос | STT + TTS (опционально) |

### 🖥️ Интерфейсы
- **Python-агент** — CLI + голос (Termux / Linux / Windows / macOS)
- **Web Dashboard** — React 19 + tRPC + Tailwind
- **Мобильное приложение** — Expo / React Native
- **Telegram-бот**
- **Live2D-аватар** в веб-клиенте
- **Minecraft-бот**

### 🔒 Безопасность
- Белый список системных команд
- Защита от Path Traversal
- Валидация ввода
- Секреты только через `.env`

---

## 🚀 Быстрый старт

### 1. Python-агент (Termux / ПК)

```bash
git clone https://github.com/fightmeb1tch99-ux/IDA.git
cd IDA
pip install -r requirements.txt
cp .env.example .env
# Добавь GROQ_API_KEY или OPENAI_API_KEY
python3 main.py
```

### Termux (Android)

```bash
pkg install python git nodejs
git clone https://github.com/fightmeb1tch99-ux/IDA.git
cd IDA
bash termux_setup.sh
nano .env   # GROQ_API_KEY=gsk_...
python main.py
```

### 2. Web Dashboard

```bash
pnpm install
pnpm dev
```

### 3. Live2D Аватар

```bash
pnpm add pixi.js@^7 pixi-live2d-display
```

Используй компонент:

```tsx
import Live2DAvatar from "@/components/Live2DAvatar";

<Live2DAvatar
  isSpeaking={isSpeaking}
  isListening={isListening}
  maxFPS={30}
  lowQuality={false}
/>
```

Модель кладётся в `client/public/live2d/ida/`.

### 4. Minecraft-компаньон

```bash
cd minecraft
npm install
```

Из Python:

```python
from minecraft import MinecraftBotManager

bot = MinecraftBotManager()
await bot.connect("play.example.com", 25565, username="IDA")
await bot.chat("Привет! Я с тобой~")
await bot.follow_player("ТвойНик")
```

Лор меняется так:

```python
bot.lore.update({
  "backstory": "Теперь я древний дух тайги...",
  "current_mood": "загадочная"
})
```

Или просто скажи IDA: «Измени свой лор на ...»

---

## 📁 Структура проекта (ключевое)

```
IDA/
├── avatar/                    # Описание и Live2D scaffold
│   ├── ida-live2d-character.json
│   └── live2d/
├── client/                    # Web Dashboard (React)
│   ├── public/live2d/ida/     # Live2D runtime files
│   └── src/components/
│       ├── Live2DAvatar.tsx   # Оптимизированный аватар
│       └── LIVE2D_INTEGRATION.md
├── minecraft/                 # Minecraft companion
│   ├── bot.js                 # Mineflayer бот
│   ├── bot_manager.py
│   ├── lore.py
│   └── package.json
├── knowledge/lore/            # Динамический лор
│   └── ida_minecraft.json
├── agents/                    # Агенты
├── plugins/                   # Плагины
├── brain.py                   # Основной мозг
├── main.py
└── README.md
```

---

## 🗺️ Roadmap

- [x] Multi-LLM + память
- [x] Web + Mobile
- [x] Live2D scaffold + оптимизация памяти
- [x] Minecraft companion (реальная игра + лор)
- [x] Discord companion (чат + голосовые + лор)
- [ ] Полноценная Live2D-модель (арт + риг)
- [ ] Голосовой lip-sync с аватаром
- [ ] Более умное поведение бота в Minecraft (добыча, строительство)
- [ ] VRM / 3D аватар

---

## 📜 Лицензия

MIT License — см. [LICENSE](LICENSE)

---

**IDA v5.1** — теперь не просто помощник, а живой компаньон.  
С аватаром. С характером. И готова зайти к тебе в Minecraft.
