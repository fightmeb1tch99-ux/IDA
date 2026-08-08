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
║     Инновационный Динамический Помощник  •  v4.0               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

# IDA — Инновационный Динамический AI-помощник

**IDA** — полноценная экосистема персонального ИИ-помощника, которая работает в терминале (Termux/ПК), веб-браузере и мобильном приложении.

**Автор:** Айтал Григорьев ([@Mareioak](https://github.com/fightmeb1tch99-ux))

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![Expo](https://img.shields.io/badge/Expo-Mobile-000020?logo=expo)](https://expo.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Возможности

### 🧠 Интеллект
- **Multi-LLM** — OpenAI, Groq, Claude, Gemini, Mistral
- Поддержка контекста и долгосрочной памяти
- Понимание команд на **русском, якутском и английском**
- RAG (работа с локальными документами) — в разработке

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
- **Web Dashboard** — React 19 + tRPC + Tailwind (киберпанк-дизайн)
- **Мобильное приложение** — Expo / React Native
- **Telegram-бот** — управление на ходу

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

# Установка зависимостей
pip install -r requirements.txt

# Настройка
cp .env.example .env
# Добавьте ключи в .env (минимум GROQ_API_KEY или OPENAI_API_KEY)

# Запуск
python3 main.py
# или
python3 brain.py
```

### 2. Web Dashboard

```bash
pnpm install
pnpm dev
# Откройте http://localhost:3000
```

### 3. Мобильное приложение

```bash
cd mobile-app   # или ida-app
npm install
npx expo start
```

Сканируйте QR-код в приложении **Expo Go**.

---

## 📁 Структура проекта

```
IDA/
├── brain.py / main.py / ida_system.py   # Ядро Python-агента
├── agents/                              # Multi-agent система
├── core/                                # Оркестратор
├── memory/                              # Система памяти
├── client/ + client-web/                # Frontend (React)
├── server/ + server-web/                # Backend (Express + tRPC)
├── mobile-app/ / ida-app/               # Expo приложение
├── drizzle/                             # Схема БД
├── requirements.txt
├── package.json
└── ...
```

> **Примечание:** В проекте есть дублирование некоторых папок (`client` / `client-web` и т.д.) — это результат активной разработки. Планируется рефакторинг.

---

## 🔑 Переменные окружения

Скопируйте `.env.example` → `.env`:

```bash
# Обязательно хотя бы один LLM
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Опционально
TELEGRAM_BOT_TOKEN=...
ALLOWED_USER_IDS=...
DATABASE_URL=...
```

---

## 🗺️ Roadmap (кратко)

- [x] Базовый агент + безопасность
- [x] Multi-LLM поддержка
- [x] Web Dashboard
- [x] Мобильное приложение
- [ ] Полноценный RAG
- [ ] Локальные LLM (Ollama)
- [ ] Улучшенный голос (Whisper + Piper)
- [ ] Multi-agent оркестрация
- [ ] Рефакторинг структуры проекта

Подробнее: [ROADMAP.md](ROADMAP.md)

---

## 🐛 Баги и предложения

Нашли баг или есть идея?  
→ Создайте [Issue](https://github.com/fightmeb1tch99-ux/IDA/issues)

---

## 📄 Лицензия

MIT License — свободно используйте и модифицируйте.

---

**Статус:** 🟢 Активная разработка  
**Последнее обновление:** Август 2026
