# 🤖 AI IDA v3.6 — IDA AI Dashboard

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-19-blue?logo=react)](https://react.dev)
[![tRPC](https://img.shields.io/badge/tRPC-11-purple?logo=trpc)](https://trpc.io)
[![Expo](https://img.shields.io/badge/Expo-Router-purple?logo=expo)](https://expo.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Open Source](https://img.shields.io/badge/Open_Source-100%25-orange)](https://github.com/fightmeb1tch99-ux/SYP-PROJECT)

**AI IDA v3.6** — полнофункциональный AI-ассистент с киберпанк-дизайном.  
Веб-Dashboard на React + tRPC с реальной интеграцией OpenAI GPT, потоковой передачей ответов, голосовой визуализацией, анимированной нейросетью и мультиязычностью (Русский, Якутский, English).

**🌐 Live Demo**: https://idadash-fctjccqe.manus.space  
**📅 Последнее обновление**: 6 июля 2026 (v3.6)  
**⭐ Версия**: 3.6 (Streaming Edition)

---

## ✨ Возможности AI IDA v3.6

| Функция | Статус | Описание |
|---|---|---|
| 💬 Реальный GPT Чат | ✅ | Потоковая передача ответов в реальном времени |
| 📊 Dashboard | ✅ | VS Code-стиль интерфейс с метриками и статистикой |
| 🎤 Голосовая визуализация | ✅ | Спектр-анализатор, реагирующий на голос в реальном времени |
| 🧠 Нейросеть анимация | ✅ | Интерактивная визуализация развития нейросети с пульсирующими нейронами |
| 📜 История чатов | ✅ | Сохранение и управление прошлыми разговорами |
| ⚙️ Управление плагинами | ✅ | Weather, Browser, Calculator с включением/отключением |
| 🌍 Мультиязычность | ✅ | Русский, Якутский (Sakha), English |
| 🔐 Аутентификация | ✅ | Email/Пароль вход, регистрация, Demo режим (30 мин) |
| 📱 Мобильная оптимизация | ✅ | Полная адаптивность для Termux и мобильных браузеров |
| 🎨 Киберпанк дизайн | ✅ | Тёмная тема с неон-эффектами (#3b82f6, #06b6d4) и микроанимациями |

---

## 🚀 Быстрый старт

### Веб-версия (рекомендуется)

Просто откройте в браузере:
```
https://idadash-fctjccqe.manus.space
```

Нажмите **"🎮 Попробовать Demo"** для временного доступа без регистрации!

### Локальная установка

#### 1. Клонировать репозиторий
```bash
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
```

#### 2. Установить зависимости

**Node.js frontend:**
```bash
cd ida-dashboard
pnpm install
```

**Python backend (опционально):**
```bash
pip install -r requirements.txt
```

#### 3. Настроить API ключ
```bash
cp .env.example .env
# Отредактируй .env и вставь свой OPENAI_API_KEY
```

#### 4. Запустить

**Web Dashboard:**
```bash
cd ida-dashboard
pnpm dev
# Откроется на http://localhost:3000
```

**Python backend (опционально):**
```bash
python3 main.py
```

---

## 📱 Мобильное приложение

### Expo Go (самый простой способ)

1. Установите **Expo Go** из Google Play Store
2. Отсканируйте QR-код проекта `ida-app`
3. Приложение загрузится и запустится на вашем телефоне

### Локальная установка

```bash
cd ida-app
npm install
npx expo start
```

---

## 🏗 Архитектура

```
AI IDA v3.6
├── Frontend (React 19 + Tailwind 4)
│   ├── Dashboard (VS Code-стиль с киберпанк-дизайном)
│   ├── Chat (потоковая передача GPT, 10ms/символ)
│   ├── Voice Visualizer (спектр-анализатор, реагирует на голос)
│   ├── Neural Network (анимированная нейросеть с пульсирующими нейронами)
│   ├── History (сохранение и управление чатами)
│   ├── Plugins (Weather, Browser, Calculator)
│   └── Settings (языки, модели, API ключ)
├── Backend (Express 4 + tRPC 11)
│   ├── OpenAI GPT интеграция с обработкой ошибок
│   ├── Аутентификация (Email/Пароль, Demo режим)
│   ├── Chat API с потоковой передачей
│   ├── Мультиязычность (i18n)
│   └── Валидация через Zod
├── Mobile (Expo Router + React Native)
│   └── Полная синхронизация с Web Dashboard
└── Python Backend (опционально)
    ├── Оркестратор агентов
    ├── Плагины (Weather, Browser, Calculator)
    └── Система памяти (SQLite)
```

---

## 🗂 Структура проекта

```
SYP-PROJECT/
├── ida-dashboard/       # 🌐 Web Dashboard (React + tRPC)
│   ├── client/          # React 19 фронтенд с киберпанк-дизайном
│   │   ├── src/pages/   # Dashboard, Chat, History, Plugins, Settings, Voice, Neural
│   │   ├── src/components/ # DashboardLayout, VoiceVisualizer, etc
│   │   └── src/index.css   # Киберпанк-стили (#0a0e1a, #3b82f6, #06b6d4)
│   ├── server/          # Express 4 + tRPC бэкенд
│   │   ├── chat.ts      # OpenAI GPT интеграция
│   │   ├── routers.ts   # tRPC процедуры
│   │   └── auth.ts      # Аутентификация
│   ├── drizzle/         # БД схема и миграции
│   └── package.json
├── ida-app/             # 📱 Мобильное приложение (Expo Router)
├── mobile-app/          # 📱 Legacy мобильное приложение
├── core/                # 🐍 Python backend
│   ├── main.py          # Точка входа
│   ├── brain.py         # NLP, парсинг, мультиязычность
│   ├── orchestrator.py  # Оркестратор агентов
│   └── ...
├── plugins/             # 🔌 Плагины (Weather, Browser, etc)
├── .env.example         # Шаблон переменных окружения
├── requirements.txt     # Python зависимости
├── Dockerfile           # Docker контейнеризация
├── docker-compose.yml   # Docker Compose (backend + frontend + db)
├── test_brain_multilingual.py  # Тесты (80%+ покрытие)
├── WEB_DASHBOARD_README.md     # Документация Dashboard
└── README.md            # Этот файл
```

---

## ⚙️ Настройка

| Параметр | Где | Описание |
|---|---|---|
| `OPENAI_API_KEY` | `.env` | Ваш OpenAI API ключ (обязателен) |
| `LLM_MODEL` | Settings | Выбор модели (GPT-4o, GPT-4o-mini) |
| `TEMPERATURE` | Settings | Температура генерации (0-1) |
| `LANGUAGE` | Settings | Язык интерфейса (Русский/Якутский/English) |
| `DATABASE_URL` | `.env` | MySQL/TiDB строка подключения |
| `JWT_SECRET` | `.env` | Секрет для сессий |

---

## 🔒 Безопасность

- 🔐 **OAuth 2.0** — Manus OAuth интеграция
- 🔑 **JWT токены** — безопасные сессии с подписью
- 🛡️ **HTTPS** — все соединения зашифрованы
- ✅ **Валидация входа** — Zod схемы для всех API запросов
- 🚫 **Rate limiting** — защита от DDoS и брутфорса
- 📝 **Логирование** — все действия записываются в логи
- 🔒 **API ключи в .env** — никогда не попадают в git

---

## 📚 Документация

- 📖 [Web Dashboard README](WEB_DASHBOARD_README.md)
- 🎨 [Design System](references/design-system.md)
- 🔌 [Backend Integration](references/backend-integration.md)
- 🌍 [Multilingual Support](references/multilingual-implementation.md)
- 🐳 [Docker Setup](references/docker-setup.md)
- 📊 [Roadmap](ROADMAP.md)

---

## 🧪 Тестирование

Запустить тесты:
```bash
# Web Dashboard
cd ida-dashboard
pnpm test

# Python backend
python -m pytest test_brain_multilingual.py -v
```

Покрытие: **80%+** ✅

---

## 🐳 Docker

Запустить всё в Docker:
```bash
docker-compose up
```

Это запустит:
- Web Dashboard на `http://localhost:3000`
- Python backend на `http://localhost:5000`
- MySQL БД на `localhost:3306`

---

## 📊 Версионирование

| Версия | Дата | Что нового |
|---|---|---|
| v3.6 | 6 июля 2026 | Потоковая передача ответов, исправление багов для Termux |
| v3.5 | 6 июля 2026 | OpenAI API интеграция, Demo режим, мобильная оптимизация |
| v3.0 | 5 июля 2026 | Web Dashboard с киберпанк-дизайном, 7 страниц функционала |
| v2.0 | 2026 | Python backend, мобильное приложение |

---

## 👤 Автор

**Григорьев Айтал Григорьевич** ([@fightmeb1tch99-ux](https://github.com/fightmeb1tch99-ux))  
Создано с ❤️ для Якутии

---

## 📄 Лицензия

MIT License — свободно используй в своих проектах!

---

*AI IDA v3.6 — 6 июля 2026*
