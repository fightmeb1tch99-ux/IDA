# 🤖 IDA — Инновационный динамический помощник v2.0

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![React Native](https://img.shields.io/badge/React_Native-Expo-purple?logo=expo)](https://expo.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Open Source](https://img.shields.io/badge/Open_Source-100%25-orange)](https://github.com/fightmeb1tch99-ux/SYP-PROJECT)

**IDA** — умный AI-агент на Python с мобильным приложением на React Native.  
Интегрируется с OpenAI GPT, умеет отвечать на вопросы, считать, показывать погоду, сохранять заметки и многое другое.

---

## ✨ Что умеет IDA v2.0

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
| LLM | Любой вопрос | GPT-ответ через OpenAI |

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
git checkout dev
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

### 3. Настроить API ключ
```bash
cp .env.example .env
# Открой .env и вставь свой OPENAI_API_KEY
```

### 4. Запустить
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
npx expo start
```

Откроется QR-код — сканируй в приложении **Expo Go** на телефоне.

---

## 🗂 Структура проекта

```
SYP-PROJECT/
├── main.py              # Точка входа, оркестратор
├── brain.py             # NLP, парсинг команд, LLM
├── config.py            # Все настройки
├── logger.py            # Логирование
├── memory_manager.py    # Память и резервные копии
├── tools/
│   └── tools.py         # Инструменты: время, погода, калькулятор...
├── memory/
│   └── memory.json      # Постоянная память агента
├── landing.html         # Лендинг-страница
├── mobile-app/          # React Native приложение
├── .env.example         # Шаблон переменных окружения
├── requirements.txt     # Python зависимости
└── README.md
```

---

## ⚙️ Настройка (config.py)

| Параметр | По умолчанию | Описание |
|---|---|---|
| `LLM_MODEL` | `gpt-5-mini` | Модель OpenAI |
| `LLM_TEMPERATURE` | `0.7` | Температура генерации |
| `CONTEXT_WINDOW` | `10` | Сколько сообщений помнит LLM |
| `ENABLE_WEATHER` | `True` | Погода через wttr.in |
| `ENABLE_CALCULATOR` | `True` | Встроенный калькулятор |
| `ENABLE_NOTES` | `True` | Система заметок |

---

## 🔒 Безопасность

- **Whitelist команд** — только разрешённые shell-команды (`ls`, `pwd`, `date` и др.)
- **Path traversal защита** — нельзя создать файл за пределами `created_files/`
- **Безопасный eval** — калькулятор использует ограниченный eval без builtins
- **Валидация ввода** — максимальная длина сообщения 4096 символов
- **.env для секретов** — API-ключи никогда не попадают в git

---

## 📚 Документация

- [README (English)](README.md)
- [README (Русский)](README_RU.md)
- [README (Саха)](README_SAH.md)
- [Гайд по установке](INSTALLATION_GUIDE.md)
- [История улучшений](IMPROVEMENTS.md)

---

## 👤 Автор

**Григорьев Айтал Григорьевич** ([@Mareioak](https://github.com/fightmeb1tch99-ux))  
Создано с ❤️ для Nothing Phone 2

---

*IDA v2.0 — 2026*
