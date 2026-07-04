# 📖 Гайд по запуску IDA на ПК и Android

Полная инструкция по установке и запуску **IDA - Инновационный динамический помощник** на разных платформах.

---

## 🖥️ Запуск на ПК (Windows, macOS, Linux)

### Требования
- Python 3.8+
- Git
- pip (идёт с Python)

### Шаг 1: Установи Python

**Windows:**
1. Скачай Python с https://www.python.org/downloads/
2. При установке **обязательно** отметь "Add Python to PATH"
3. Нажми "Install Now"

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip git
```

### Шаг 2: Клонируй репозиторий

```bash
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
git checkout dev
```

### Шаг 3: Установи зависимости

```bash
pip install -r requirements.txt
```

Или если не работает:
```bash
pip3 install -r requirements.txt
```

### Шаг 4: Добавь OpenAI API ключ

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ
```

**macOS/Linux:**
```bash
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"
```

### Шаг 5: Запусти IDA

**Интерактивный режим:**
```bash
python3 main.py
```

Потом введи свой запрос и нажми Enter.

**Одна команда:**
```bash
python3 main.py "Привет, как дела?"
python3 main.py "Сколько сейчас времени?"
python3 main.py "Создай файл test.txt"
```

### Полезные команды

| Команда | Результат |
|---------|-----------|
| `python3 main.py --help` | Справка |
| `python3 main.py --stats` | Статистика |
| `python3 main.py "Привет"` | Отправить сообщение |

---

## 📱 Запуск на Android (Nothing Phone 2)

### Способ 1: Через Termux (Рекомендуется)

#### Требования
- Termux (скачай из F-Droid или Google Play Store)
- Интернет соединение
- ~500 МБ свободного места

#### Установка

**Шаг 1: Открой Termux**

**Шаг 2: Обнови пакеты**
```bash
pkg update && pkg upgrade -y
```

**Шаг 3: Установи необходимое**
```bash
pkg install python git -y
```

**Шаг 4: Клонируй проект**
```bash
cd ~
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
git checkout dev
```

**Шаг 5: Установи зависимости**
```bash
pip install -r requirements.txt
```

**Шаг 6: Добавь API ключ**
```bash
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"
```

Чтобы ключ сохранялся автоматически:
```bash
echo 'export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"' >> ~/.bashrc
source ~/.bashrc
```

**Шаг 7: Запусти IDA**
```bash
python3 main.py
```

---

### Способ 2: Мобильное приложение (Красивый интерфейс)

#### Требования
- Expo Go (скачай из Google Play Store)
- Node.js и npm (установи в Termux)
- ~1 ГБ свободного места

#### Установка

**Шаг 1: Установи Node.js в Termux**
```bash
pkg install nodejs -y
npm install -g pnpm
```

**Шаг 2: Перейди в папку приложения**
```bash
cd ~/SYP-PROJECT/mobile-app
```

**Шаг 3: Установи зависимости**
```bash
pnpm install
```

Или если не работает:
```bash
npm install
```

**Шаг 4: Запусти сервер**
```bash
pnpm dev
```

Или:
```bash
npm start
```

**Шаг 5: Отсканируй QR-код**
1. Открой **Expo Go** на телефоне
2. Нажми кнопку **"Scan QR code"** (камера)
3. Наведи на QR-код в Termux
4. Приложение загрузится автоматически! 🎉

**Шаг 6: Добавь API ключ**
В файле `App.js` найди строку:
```javascript
const OPENAI_API_KEY = 'sk-proj-...';
```

Замени на свой ключ:
```javascript
const OPENAI_API_KEY = 'sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ';
```

Сохрани и приложение обновится автоматически.

---

### Способ 3: Собрать APK (Постоянная установка)

Это создаст файл `.apk` который можно установить как обычное приложение.

**Требования:**
- Java Development Kit (JDK)
- Android SDK
- ~3 ГБ свободного места

**Установка:**

```bash
cd ~/SYP-PROJECT/mobile-app
npm install -g eas-cli
eas build --platform android --local
```

После завершения (может занять 10-20 минут) будет создан файл `.apk`.

Скачай его и установи на телефон:
```bash
# Найди файл .apk в папке dist/
# Скопируй его на телефон
# Открой файловый менеджер
# Нажми на .apk файл
# Нажми "Установить"
```

---

## 🔧 Решение проблем

### Проблема: "Python не найден"

**Windows:**
1. Проверь что Python установлен: `python --version`
2. Если не работает, переустанови Python
3. При переустановке отметь "Add Python to PATH"

**macOS/Linux:**
```bash
which python3
python3 --version
```

### Проблема: "pip не найден"

```bash
python3 -m pip install -r requirements.txt
```

### Проблема: "OpenAI API ошибка"

1. Проверь что ключ установлен:
```bash
echo $OPENAI_API_KEY
```

2. Если пусто, добавь ключ снова:
```bash
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"
```

3. Убедись что ключ правильный на https://platform.openai.com/api-keys

### Проблема: "Expo Go несовместим"

1. Обнови Expo Go из Google Play Store
2. Или удали и переустанови
3. Понизь версию Expo в проекте:
```bash
cd mobile-app
npm install expo@49
npm start
```

### Проблема: "Медленная работа в Termux"

Это нормально! Termux работает медленнее чем полноценный ПК.

Решения:
- Закрой другие приложения
- Используй более простые команды
- Запусти на ПК если возможно

---

## 📊 Сравнение способов запуска

| Способ | Сложность | Скорость | Интерфейс | Рекомендуется |
|--------|-----------|----------|-----------|---------------|
| **ПК (Python)** | ⭐ Легко | ⭐⭐⭐ Быстро | 📝 Текст | Для разработки |
| **Termux (Python)** | ⭐⭐ Средне | ⭐⭐ Медленно | 📝 Текст | Для тестирования |
| **Expo Go** | ⭐⭐ Средне | ⭐⭐ Медленно | 🎨 Красивый | Для демо |
| **APK** | ⭐⭐⭐ Сложно | ⭐⭐⭐ Быстро | 🎨 Красивый | Для использования |

---

## 🚀 Быстрый старт

### На ПК (самый быстрый способ):
```bash
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
git checkout dev
pip install -r requirements.txt
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ"
python3 main.py
```

### На Android (Termux):
```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT && git checkout dev
pip install -r requirements.txt
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ"
python3 main.py
```

### На Android (Мобильное приложение):
```bash
pkg install nodejs -y
npm install -g pnpm
cd ~/SYP-PROJECT/mobile-app
pnpm install
pnpm dev
# Отсканируй QR-код в Expo Go
```

---

## 📞 Если что-то не работает

1. **Проверь интернет** - нужен для OpenAI API
2. **Проверь API ключ** - должен быть валидным
3. **Обнови зависимости** - `pip install --upgrade -r requirements.txt`
4. **Посмотри логи** - в папке `logs/`
5. **Создай issue на GitHub** - https://github.com/fightmeb1tch99-ux/SYP-PROJECT/issues

---

**Создатель:** Григорьев Айтал Григорьевич (@Mareioak)  
**Версия:** 0.1.0  
**Последнее обновление:** 2026-07-04
