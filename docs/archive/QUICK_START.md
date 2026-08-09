# 🚀 Быстрый старт IDA v 0.1

**Статус:** ✅ Все протестировано и работает!

Выбери свою платформу и следуй инструкциям.

---

## 💻 На ПК (Windows, macOS, Linux)

### ⏱️ Время: 5 минут

#### Шаг 1: Установи Python 3.8+
- **Windows:** https://www.python.org/downloads/ (отметь "Add to PATH")
- **macOS:** `brew install python3`
- **Linux:** `sudo apt install python3 python3-pip git`

#### Шаг 2: Клонируй проект
```bash
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
git checkout dev
```

#### Шаг 3: Установи зависимости
```bash
pip install -r requirements.txt
```

#### Шаг 4: Добавь OpenAI API ключ
```bash
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"
```

#### Шаг 5: Запусти IDA
```bash
python3 main.py
```

**Готово!** Теперь введи любой вопрос и нажми Enter.

#### Примеры команд:
```bash
python3 main.py "Привет, как дела?"
python3 main.py "Сколько сейчас времени?"
python3 main.py "Создай файл test.txt"
python3 main.py --help
```

---

## 📱 На Android (Nothing Phone 2)

### Способ 1: Termux (Текстовый чат) ⏱️ 10 минут

#### Требования:
- Termux (F-Droid или Google Play Store)
- Интернет
- 500 МБ свободного места

#### Установка:

**Шаг 1:** Открой Termux

**Шаг 2:** Обнови пакеты
```bash
pkg update && pkg upgrade -y
```

**Шаг 3:** Установи Python
```bash
pkg install python git -y
```

**Шаг 4:** Клонируй проект
```bash
git clone https://github.com/fightmeb1tch99-ux/SYP-PROJECT
cd SYP-PROJECT
git checkout dev
```

**Шаг 5:** Установи зависимости
```bash
pip install -r requirements.txt
```

**Шаг 6:** Добавь API ключ
```bash
export OPENAI_API_KEY="sk-proj-ТВО_КЛЮЧ_ЗДЕСЬ"
```

**Шаг 7:** Запусти IDA
```bash
python3 main.py
```

✅ **Готово!** Общайся с IDA в Termux.

---

### Способ 2: Мобильное приложение (Красивый интерфейс) ⏱️ 15 минут

#### Требования:
- Expo Go (Google Play Store)
- Node.js в Termux
- 1 ГБ свободного места

#### Установка:

**Шаг 1:** Установи Node.js в Termux
```bash
pkg install nodejs -y
npm install -g pnpm
```

**Шаг 2:** Перейди в папку приложения
```bash
cd ~/SYP-PROJECT/mobile-app
```

**Шаг 3:** Установи зависимости
```bash
pnpm install
```

**Шаг 4:** Запусти сервер
```bash
pnpm dev
```

**Шаг 5:** Отсканируй QR-код
1. Открой **Expo Go** на телефоне
2. Нажми **"Scan QR code"** (камера)
3. Наведи на QR-код в Termux
4. Приложение загрузится! 🎉

**Шаг 6:** Добавь API ключ
В файле `mobile-app/App.js` найди:
```javascript
const OPENAI_API_KEY = 'sk-proj-...';
```

Замени на свой ключ и сохрани. Приложение обновится автоматически.

✅ **Готово!** Используй красивое мобильное приложение.

---

### Способ 3: APK (Постоянная установка) ⏱️ 20 минут

Это создаст приложение как обычное Android приложение.

```bash
cd ~/SYP-PROJECT/mobile-app
npm install -g eas-cli
eas build --platform android --local
```

После завершения:
1. Найди файл `.apk` в папке `dist/`
2. Скопируй на телефон
3. Открой файловый менеджер
4. Нажми на `.apk` файл
5. Нажми "Установить"

✅ **Готово!** Приложение установлено как обычное приложение.

---

## 🎯 Как получить OpenAI API ключ?

1. Открой https://platform.openai.com/api-keys
2. Нажми "Create new secret key"
3. Скопируй ключ (начинается с `sk-proj-`)
4. **⚠️ НИКОМУ НЕ ПОКАЗЫВАЙ КЛЮЧ!**
5. Используй в команде `export OPENAI_API_KEY="sk-proj-..."`

---

## ✅ Проверка что всё работает

### На ПК:
```bash
python3 main.py "Привет"
```
Должна быть ответ от IDA.

### На Android (Termux):
```bash
python3 main.py "Привет"
```
Должна быть ответ от IDA.

### На Android (Expo Go):
1. Открой приложение
2. Напиши сообщение
3. Нажми отправить
4. Должен быть ответ

---

## 🆘 Если что-то не работает

### "Python не найден"
```bash
python3 --version
```
Если не работает, переустанови Python.

### "pip не найден"
```bash
python3 -m pip install -r requirements.txt
```

### "OpenAI API ошибка"
```bash
echo $OPENAI_API_KEY
```
Если пусто, добавь ключ снова.

### "Expo Go несовместим"
Обнови Expo Go из Google Play Store.

### "Медленно работает"
Это нормально для Termux. Закрой другие приложения.

---

## 📊 Сравнение способов

| Способ | Сложность | Скорость | Интерфейс | Рекомендуется |
|--------|-----------|----------|-----------|---------------|
| ПК | ⭐ Легко | ⭐⭐⭐ Быстро | 📝 Текст | Для разработки |
| Termux | ⭐⭐ Средне | ⭐⭐ Медленно | 📝 Текст | Для тестирования |
| Expo Go | ⭐⭐ Средне | ⭐⭐ Медленно | 🎨 Красивый | Для демо |
| APK | ⭐⭐⭐ Сложно | ⭐⭐⭐ Быстро | 🎨 Красивый | Для использования |

---

## 🎉 Готово!

Выбери способ, который тебе нравится, и начни использовать IDA!

**Создатель:** Григорьев Айтал Григорьевич (@Mareioak)  
**Версия:** 0.1.0  
**Статус:** ✅ Production Ready
