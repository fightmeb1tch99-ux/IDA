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
║        Инновационный Динамический Помощник                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

# IDA — AI Assistant Ecosystem

**IDA** (Инновационный Динамический Помощник) — полноценная экосистема ИИ-помощника с поддержкой нескольких LLM, веб-дашбордом, мобильным приложением и Python-агентом.

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue?logo=typescript)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev)
[![Expo](https://img.shields.io/badge/Expo-Mobile-000020?logo=expo)](https://expo.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Автор:** Айтал Григорьев ([@Mareioak](https://github.com/fightmeb1tch99-ux))

---

## Возможности

### Python-агент (Termux / ПК)
- Работа с несколькими LLM: **OpenAI**, **Groq**, Claude, Gemini, Mistral
- Инструменты: погода, калькулятор, заметки, поиск, работа с файлами, системные команды (whitelist)
- Долговременная память
- Голосовой ввод/вывод (опционально)
- AI Camera Brain — анализ с камеры + обучение

### Web Dashboard
- Современный интерфейс (React 19 + tRPC + Tailwind)
- Реал-тайм чат с потоковой передачей
- Выбор провайдера и модели
- История, настройки, визуализации

### Мобильное приложение
- React Native + Expo
- Тёмная тема, быстрые команды, история чатов

### Безопасность
- Whitelist системных команд
- Защита от Path Traversal
- Валидация ввода
- Секреты только через `.env`

---

## Быстрый старт

### 1. Клонирование
```bash
git clone https://github.com/fightmeb1tch99-ux/IDA.git
cd IDA
```

### 2. Python-агент
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Отредактируй .env и добавь ключи:
# OPENAI_API_KEY=sk-...
# GROQ_API_KEY=gsk_...

python main.py
# или
python brain.py
```

### 3. Web Dashboard
```bash
pnpm install          # или npm install
pnpm dev              # http://localhost:3000
```

### 4. Мобильное приложение
```bash
cd mobile-app         # или ida-app
npm install
npx expo start
```

---

## Структура проекта (упрощённо)

```
IDA/
├── main.py / brain.py / ida_system.py   # Ядро Python-агента
├── agents/                              # Multi-agent система
├── core/                                # Оркестратор
├── client/ + client-web/                # Frontend (React)
├── server/ + server-web/                # Backend (Express + tRPC)
├── mobile-app/ / ida-app/               # Expo приложение
├── memory/                              # Память агента
├── requirements.txt
├── package.json
└── LICENSE
```

> **Примечание:** В репозитории пока есть дублирование папок (`client` / `client-web` и т.д.) — это технический долг, который планируется почистить.

---

## Переменные окружения

Скопируй `.env.example` → `.env`:

```env
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
# TELEGRAM_BOT_TOKEN=...
# ALLOWED_USER_IDS=...
```

---

## Roadmap (кратко)

- [x] Базовый агент + инструменты + безопасность
- [x] Multi-LLM поддержка
- [x] Web Dashboard
- [x] Мобильное приложение (Expo)
- [x] AI Camera Brain
- [ ] Полная очистка структуры репозитория
- [ ] RAG по локальным документам
- [ ] Локальные LLM через Ollama
- [ ] Telegram-бот (полная синхронизация)
- [ ] Multi-agent оркестрация

---

## Лицензия

[MIT](LICENSE) — можно свободно использовать, изменять и распространять.

---

**Статус:** Активная разработка  
**Последнее обновление документации:** Август 2026
