# IDA Live2D Avatar

Структура модели для Live2D Cubism (версия 4 / 5).

## Текущий статус

Это **заглушка / scaffold**.  
Файл `.moc3` и текстуры ещё не созданы — их нужно сделать в Live2D Cubism Editor.

## Как сделать настоящую модель (пошагово)

1. **Скачайте Live2D Cubism Editor**  
   https://www.live2d.com/en/download/cubism/  
   (есть бесплатная версия Cubism Editor 5)

2. **Подготовьте арт**  
   - Нарисуйте или сгенерируйте персонажа в стиле, описанном в `../ida-live2d-character.json`
   - Разбейте на слои (PSD): волосы, лицо, глаза, рот, тело, платье, шляпа и т.д.
   - Рекомендуемый размер текстуры: 2048×2048

3. **Импорт в Cubism**  
   - File → New → Import PSD  
   - Расставьте деформаторы (Warp / Rotation)  
   - Настройте параметры:  
     - ParamAngleX / Y / Z  
     - ParamEyeLOpen / ParamEyeROpen  
     - ParamMouthOpenY  
     - ParamBreath

4. **Физика**  
   - Добавьте Physics для длинных волос и платья

5. **Экспорт**  
   - File → Export → Embed File (или Runtime)  
   - Положите файлы в эту папку:
     - `ida.moc3`
     - `ida.2048/texture_00.png`
     - остальные файлы уже есть

6. **Подключение в проекте IDA**  
   Рекомендуемый путь: `client/public/live2d/ida/`  
   Библиотека: `pixi-live2d-display` или официальный Cubism Web SDK

## Структура файлов

```
ida/
├── ida.model3.json          ← главный файл модели
├── ida.moc3                 ← (нужно создать в Cubism)
├── ida.physics3.json
├── ida.pose3.json
├── ida.cdi3.json
├── ida.2048/
│   └── texture_00.png       ← (нужно создать)
├── expressions/
│   ├── neutral.exp3.json
│   ├── happy.exp3.json
│   ├── thinking.exp3.json
│   ├── listening.exp3.json
│   └── speaking.exp3.json
└── motions/
    ├── idle_01.motion3.json
    ├── idle_02.motion3.json
    ├── talk_01.motion3.json
    ├── talk_02.motion3.json
    └── listen_01.motion3.json
```

## Быстрый тест в браузере

После того как появятся `.moc3` + текстура, можно использовать:

```html
<script src="https://cdn.jsdelivr.net/npm/pixi-live2d-display/dist/index.min.js"></script>
```

или React-компонент с `pixi-live2d-display`.

## Связанные файлы

- Описание персонажа: `../ida-live2d-character.json`
- Roadmap: `../../docs/AVATAR_ROADMAP.md`
