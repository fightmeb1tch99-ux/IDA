# Голос IDA — путь к качественному realtime voice

## Сейчас
- `pyttsx3` (offline TTS, качество среднее)
- `SpeechRecognition` + Google/Sphinx (STT)

## Следующий уровень (рекомендуется)

### STT — Whisper
```bash
pip install openai-whisper
# или faster-whisper
```

### TTS — Piper (быстрый, локальный, качественный)
```bash
# Скачать модель с https://github.com/rhasspy/piper
# Русские модели есть
```

### Альтернативы
- Kokoro TTS
- ElevenLabs (облако, очень качественно)
- OpenAI TTS

## Realtime (как у AIRI / ChatGPT Voice)
1. VAD (Voice Activity Detection)
2. Streaming STT
3. LLM streaming
4. Streaming TTS
5. WebSocket / WebRTC между клиентом и агентом

Файл `realtime/bridge.py` — заготовка WebSocket-моста.
