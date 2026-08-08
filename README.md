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
║        Инновационный Динамический Помощник v3.7              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

# AI IDA - Multi-LLM Assistant Ecosystem

**AI IDA** — это полнофункциональная экосистема ИИ-помощника с поддержкой нескольких LLM провайдеров, веб-панелью управления и мобильным приложением.

## 🌟 Возможности

### 🎨 Web Dashboard (v3.7)
- **Киберпанк-дизайн** с цветовой схемой (#0a0e1a, #3b82f6, #06b6d4)
- **Multi-LLM интеграция**: OpenAI, Claude, Gemini, Groq, Mistral
- **Реал-тайм чат** с потоковой передачей (10ms/char)
- **Интерактивные вкладки**:
  - 💬 Chat — общение с ИИ
  - 📊 Dashboard — статистика и метрики
  - 🧠 Neural Network — визуализация нейросети
  - 🎤 Voice — анализ голоса в реальном времени
  - 📜 History — история разговоров
  - ⚙️ Settings — выбор провайдера и модели

### 📱 Mobile App (Expo)
- React Native с Expo Router
- Полная адаптивность под мобильные устройства
- Termux-оптимизированный интерфейс

### 🐍 Python Backend
- Агент-ориентированная архитектура
- Поддержка множества команд и инструментов
- Сохранение памяти и истории

## 🚀 Быстрый старт

### Web Dashboard
```bash
cd ida-dashboard
pnpm install
pnpm dev
# Откройте http://localhost:3000
```

### Python Agent (Termux)
```bash
# Установите зависимости
pip install -r requirements.txt

# Установите OpenAI API ключ
export OPENAI_API_KEY="sk-proj-..."

# Запустите агента
python3 brain.py
```

## 📋 Поддерживаемые LLM Провайдеры

| Провайдер | Модели | Статус |
|-----------|--------|--------|
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-4-turbo | ✅ Активно |
| **Claude** | claude-3-5-sonnet, claude-3-opus | ✅ Готово |
| **Gemini** | gemini-2.0-flash, gemini-1.5-pro | ✅ Готово |
| **Groq** | mixtral-8x7b, llama-3-70b | ✅ Готово |
| **Mistral** | mistral-large, mistral-medium | ✅ Готово |

## 🎯 Текущая версия: v3.7

### Что нового в v3.7
- ✅ Фиксированы TypeScript ошибки
- ✅ Реализована Multi-LLM поддержка
- ✅ Settings UI для выбора провайдера
- ✅ Потоковая передача ответов
- ✅ Поддержка русского, якутского и английского языков

### Следующие шаги (v3.8)
- 🔄 Сохранение настроек в БД
- 🔄 Динамическое переключение провайдеров
- 🔄 API ключ валидация
- 🔄 Расширенная аналитика

## 📂 Структура проекта

```
SYP-PROJECT/
├── ida-dashboard/          # Web Dashboard (React + tRPC)
│   ├── client/            # Frontend (React 19)
│   ├── server/            # Backend (Express + tRPC)
│   ├── drizzle/           # Database schema
│   └── references/        # Integration docs
├── agents/                # Python агенты
├── brain.py              # Основной агент
├── config.py             # Конфигурация
└── README.md             # Этот файл
```

## 🔐 Переменные окружения

```bash
# OpenAI API
OPENAI_API_KEY=sk-proj-...
OPENAI_API_BASE=https://api.manus.im/api/llm-proxy/v1

# Database
DATABASE_URL=mysql://user:pass@localhost/ida

# Web Dashboard
VITE_APP_ID=...
VITE_OAUTH_PORTAL_URL=...
JWT_SECRET=...
```

## 🛠️ Технологический стек

### Frontend
- React 19 + Tailwind CSS 4
- tRPC для типобезопасного API
- Wouter для маршрутизации
- Sonner для уведомлений

### Backend
- Express 4 + Node.js
- Drizzle ORM + MySQL
- OpenAI SDK + LLM интеграции
- Manus OAuth

### Mobile
- Expo Router
- React Native
- TypeScript

### Python
- OpenAI API
- DuckDuckGo Web Search
- File Management
- Memory System

## 📝 Лицензия

MIT License — свободно используй и модифицируй!

## 👨‍💻 Автор

**Айтал Григорьев** — разработчик AI IDA

---

**Статус проекта**: 🟢 Активная разработка

**Последнее обновление**: 2026-07-07

**Версия**: 3.7 (Multi-LLM Integration Phase 1)
