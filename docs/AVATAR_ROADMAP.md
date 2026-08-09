# Аватар IDA — путь к Live2D / VRM

## Сейчас
- `AvatarPresence` — киберпанк-круг с анимацией «говорит / слушает»
- `VoiceVisualizer` — визуализация частот голоса

## Следующие шаги

1. **Простой 2D аватар**
   - Статичная картинка / спрайт-анимация рта
   - Lip-sync по громкости аудио

2. **Live2D**
   - Cubism SDK 4/5
   - Модель `.model3.json` + textures
   - Библиотеки: `pixi-live2d-display` (веб) или Cubism Native

3. **VRM (3D)**
   - Three.js + `@pixiv/three-vrm`
   - Авто-моргание, look-at, idle анимации
   - Как в AIRI

Рекомендация: начать с Live2D — проще и легче для веб/мобилки.
