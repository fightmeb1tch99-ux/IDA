# 🚀 Инструкция по развертыванию IDA в облаке

Теперь ты можешь запустить IDA так, чтобы она была доступна **по ссылке в браузере** 24/7!

---

## 🌐 Вариант 1: Публичная ссылка (Web Chat) через Render.com
*Рекомендуется для доступа с любого устройства.*

1.  **Создай аккаунт** на [Render.com](https://render.com/).
2.  Нажми **New +** -> **Web Service**.
3.  Подключи свой GitHub репозиторий `SYP-PROJECT`.
4.  **Настройки:**
    - **Runtime:** `Python 3`
    - **Build Command:** `pip install -r requirements.txt`
    - **Start Command:** `python web_dashboard.py`
5.  **Environment Variables (Важно!):** Нажми "Advanced" и добавь:
    - `OPENAI_API_KEY`: твой ключ.
    - `TELEGRAM_BOT_TOKEN`: если хочешь, чтобы бот тоже работал (см. Docker ниже).
6.  **Готово!** После деплоя ты получишь ссылку типа `https://syp-project.onrender.com`. Открой её — и твой ИИ в браузере!

---

## 🤖 Вариант 2: Запуск и Бота, и Веб-чата (Docker)
*Если хочешь, чтобы работало всё сразу.*

На Render выбери **Runtime: Docker**. Render сам увидит `Dockerfile` и запустит обе системы параллельно.

---

## 📱 Вариант 3: Только API для мобильного приложения
*Если тебе нужен только бэкенд для телефона.*

Используй **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app`.

---

## 🛠 Обновление ссылок

После деплоя не забудь обновить URL в мобильном приложении (`mobile-app/App.js`):
```javascript
const SERVER_URL = 'https://твой-проект.onrender.com/v1/chat'; 
```

**Теперь твоя IDA — это настоящий облачный интеллект!** 🌍🦾✨
