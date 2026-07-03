# IDA v 0.1 - Mobile App

Мобильное приложение для AI ассистента IDA с красивым интерфейсом.

## Установка

### В Termux на Nothing Phone 2:

```bash
cd ~/SYP_PROJECT/mobile-app
npm install
npm start
```

Или с pnpm:

```bash
cd ~/SYP_PROJECT/mobile-app
pnpm install
pnpm dev
```

## Настройка OpenAI API

1. Открой файл `App.js`
2. Найди строку: `const OPENAI_API_KEY = 'sk-proj-...';`
3. Замени на свой API ключ от OpenAI

## Запуск на телефоне

1. Установи **Expo Go** из Google Play Store
2. Запусти приложение командой выше
3. Отсканируй QR-код в Expo Go
4. Приложение загрузится на телефон!

## Функции

✅ Красивый чат интерфейс  
✅ Интеграция с OpenAI GPT  
✅ История сообщений  
✅ Темная тема  
✅ Быстрые ответы  

## Структура

```
mobile-app/
├── App.js           # Главный компонент приложения
├── app.json         # Конфигурация Expo
├── package.json     # Зависимости
└── assets/          # Иконки и изображения
```

## Требования

- Node.js 16+
- npm или pnpm
- Expo Go (на телефоне)
- OpenAI API ключ

Enjoy! 🚀
