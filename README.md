# 🤖 IDA — Инновационный динамический помощник v4.0

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![React Native](https://img.shields.io/badge/React_Native-Expo-purple?logo=expo)](https://expo.dev)
[![Groq API](https://img.shields.io/badge/Groq-API-orange)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Open Source](https://img.shields.io/badge/Open_Source-100%25-orange)](https://github.com/fightmeb1tch99-ux/SYP-PROJECT)

**IDA v4.0** — умный AI-агент на Python с мобильным приложением на React Native.  
Интегрируется с **Groq API** (бесплатный LLM), умеет отвечать на вопросы, считать, показывать погоду, сохранять заметки и многое другое.

**Создатель:** Григорьев Айтал Григорьевич (@Mareioak)

---

## ✨ Что умеет IDA v4.0

| Команда | Пример | Описание |
|---|---|---|
| Время | `Какое время?` | Текущее время |
| Дата | `Какая дата?` | Текущая дата |
| Погода | `Какая погода?` | Погода через wttr.in (без ключа) |
| Калькулятор | `Посчитай 15 * 7 + 3` | Безопасное вычисление |
| Заметки | `Запомни купить молоко` | Сохранение заметок |
| Поиск | `Найди Python туториал` | DuckDuckGo поиск |
| Файлы | `Создай файл notes.txt` | Создание файлов |
| Команды | `Выполни ls` | Безопасные shell-команды |
| Личное | `Меня зовут Айтал` | Запоминание имени |
| Голос | `Редактор` или `Editor` | Интерактивный редактор кода |
| LLM | Любой вопрос | **Groq API** ответ (бесплатно!) |

### 🎉 Новое в v4.0

- ✅ **Groq API** — Бесплатный и быстрый LLM вместо OpenAI
- ✅ **ASCII загрузка** — Красивая анимация пончика в Termux
- ✅ **Редактор кода** — Пишите код прямо в консоли
- ✅ **Голосовой помощник** — Распознавание и синтез речи
- ✅ **Мобильное приложение** — React Native + Expo с темной темой
- ✅ **Веб-страница** — Красивый лэндинг для браузера
- ✅ **Проверка стиля** — Clang Format, ESLint, Pylint
- ✅ **Полная документация** — На русском, якутском и английском

---

## 🚀 Быстрый старт

### На Android (Termux)

```bash
# 1. Установи зависимости
pkg install python git -y
pip install groq

# 2. Клонируй проект
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT IDA
cd IDA
git checkout dev

# 3. Установи Groq API ключ
export GROQ_API_KEY="gsk_..."

# 4. Запусти IDA
python3 main.py
```

### На ПК (Windows/macOS/Linux)

```bash
# 1. Установи Python 3.9+
# https://www.python.org/downloads/

# 2. Клонируй проект
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT IDA
cd IDA
git checkout dev

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Установи Groq API ключ
export GROQ_API_KEY="gsk_..."

# 5. Запусти IDA
python3 main.py
```

### Запуск IDA

```bash
# Интерактивный режим
python3 main.py

# Одна команда
python3 main.py "Какое время?"

# Справка
python3 main.py --help

# Статистика
python3 main.py --stats
```

---

## 📱 Мобильное приложение

```bash
cd mobile-app
npm install
npm start
```

Откроется QR-код — сканируй в приложении **Expo Go** на телефоне.

### Возможности мобильного приложения

- 🎨 Темная тема (futuristic design)
- 🎤 Голосовой помощник с анимацией
- ⚡ Быстрые команды
- 💾 Сохранение истории чатов
- 🌙 Переключатель темы

---

## 🌐 Веб-страница

Открой `landing.html` в браузере для красивого лэндинга проекта.

---

## 🗂 Структура проекта

```
IDA/
├── main.py                  # Точка входа, оркестратор
├── brain.py                 # NLP, парсинг команд, LLM (Groq)
├── groq_client.py           # Groq API клиент
├── config.py                # Все настройки
├── logger.py                # Логирование
├── ida_system.py            # Системные инструменты
├── tools/
│   └── tools.py             # Инструменты: время, погода, калькулятор...
├── memory/
│   └── memory.json          # Постоянная память агента
├── landing.html             # Лендинг-страница
├── mobile-app/              # React Native приложение (Expo)
├── README_V4.md             # Полная документация v4.0
├── README_RU.md             # README на русском
├── README_SAH.md            # README на якутском
├── .env.example             # Шаблон переменных окружения
├── requirements.txt         # Python зависимости
└── README.md                # Этот файл
```

---

## ⚙️ Настройка (config.py)

| Параметр | По умолчанию | Описание |
|---|---|---|
| `LLM_MODEL` | `mixtral-8x7b-32768` | Модель Groq |
| `LLM_TEMPERATURE` | `0.7` | Температура генерации |
| `CONTEXT_WINDOW` | `10` | Сколько сообщений помнит LLM |
| `ENABLE_WEATHER` | `True` | Погода через wttr.in |
| `ENABLE_CALCULATOR` | `True` | Встроенный калькулятор |
| `ENABLE_NOTES` | `True` | Система заметок |
| `GROQ_API_KEY` | `env` | Ключ Groq API |

---

## 🔒 Безопасность

- **Whitelist команд** — только разрешённые shell-команды (`ls`, `pwd`, `date` и др.)
- **Path traversal защита** — нельзя создать файл за пределами `created_files/`
- **Безопасный eval** — калькулятор использует ограниченный eval без builtins
- **Валидация ввода** — максимальная длина сообщения 4096 символов
- **.env для секретов** — API-ключи никогда не попадают в git
- **Защита от инъекций** — Groq API защищен от prompt injection

---

## 🎮 Будущие обновления

### v5.0 - Minecraft Integration
- 🎮 Встроенная игра Minecraft
- 🏗️ Строительство и исследование
- 💬 Общение с ИИ во время игры
- 🎨 Кастомные текстуры

**Ветка:** `feature/minecraft-game`

### v6.0 - Terraria Integration
- 🎮 Встроенная игра Terraria
- ⚔️ Боевая система
- 🎁 Система предметов
- 🗺️ Процедурная генерация миров

**Ветка:** `feature/terraria-game`

### v7.0 - Multiplayer
- 👥 Сетевая игра
- 🌐 Облачное хранилище
- 🏆 Рейтинги и достижения
- 💬 Чат между игроками

**Ветка:** `feature/multiplayer`

---

## 🌳 Структура веток

| Ветка | Описание | Статус |
|-------|---------|--------|
| `main` | Стабильная версия для продакшена | ✅ Активна |
| `dev` | Текущая разработка (v4.0) | ✅ Активна |
| `feature/minecraft-game` | Интеграция Minecraft (v5.0) | 🔄 В разработке |
| `feature/terraria-game` | Интеграция Terraria (v6.0) | 📋 Планируется |
| `feature/multiplayer` | Многопользовательская игра (v7.0) | 📋 Планируется |

---

## 📚 Документация

- [README (English)](README.md) — этот файл
- [README (Русский)](README_RU.md) — на русском языке
- [README (Саха)](README_SAH.md) — на якутском языке
- [Полная документация v4.0](README_V4.md) — все детали
- [Гайд по установке](INSTALLATION_GUIDE.md) — пошаговая инструкция
- [История улучшений](IMPROVEMENTS.md) — что было сделано

---

## 👤 Автор

**Григорьев Айтал Григорьевич** ([@Mareioak](https://github.com/fightmeb1tch99-ux))  
Создано с ❤️ для Nothing Phone 2

---

## 📝 Лицензия

MIT License — свободно используй в своих проектах!

---

*IDA v4.0 — 2026*
