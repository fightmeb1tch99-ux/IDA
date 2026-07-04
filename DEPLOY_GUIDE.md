# 🚀 Инструкция по развертыванию сервера IDA в облаке

Чтобы твое мобильное приложение работало везде, нужно запустить `server.py` на облачном хостинге. Вот лучшие варианты:

---

## Вариант 1: Render (Рекомендуется)
*Бесплатно, просто, поддерживает FastAPI.*

1. Создай аккаунт на [Render.com](https://render.com/).
2. Нажми **New +** -> **Web Service**.
3. Подключи свой GitHub репозиторий `SYP-PROJECT`.
4. Настройки:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app`
5. В разделе **Environment Variables** добавь:
   - `OPENAI_API_KEY`: твой ключ от OpenAI.
   - `IDA_MODEL`: `gpt-5-mini` (или другую).
6. После деплоя ты получишь URL типа `https://syp-project.onrender.com`.

---

## Вариант 2: Vercel
*Быстро, отлично подходит для API.*

1. Установи Vercel CLI: `npm i -g vercel`.
2. Запусти команду `vercel` в корне проекта.
3. В настройках проекта на сайте Vercel добавь `OPENAI_API_KEY` в **Environment Variables**.
4. URL будет типа `https://syp-project.vercel.app`.

---

## Вариант 3: Heroku
*Классика, но требует привязки карты.*

1. Создай приложение в Heroku Dashboard.
2. В разделе **Settings** -> **Config Vars** добавь свой `OPENAI_API_KEY`.
3. Подключи GitHub и нажми **Deploy Branch**.

---

## 📱 Обновление мобильного приложения

После того как сервер запустится в облаке, не забудь обновить адрес в `mobile-app/App.js`:

```javascript
// Замени на URL своего облачного сервера
const SERVER_URL = 'https://твой-проект.onrender.com/v1/chat'; 
```

---

**Теперь твоя IDA доступна 24/7 по всему миру!** 🌍🦾
