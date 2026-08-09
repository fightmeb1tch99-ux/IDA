# Realtime Bridge

## Запуск

```bash
pip install fastapi uvicorn websockets
python -m realtime.bridge
# → ws://0.0.0.0:8765/ws
# → http://0.0.0.0:8765/health
# → POST http://0.0.0.0:8765/chat  {"message": "привет"}
```

## Протокол WebSocket

Клиент → сервер:
```json
{"type": "chat", "message": "Какая погода в Якутске?"}
```

Сервер → клиент:
```json
{"type": "status", "data": {"thinking": true}}
{"type": "chat", "data": {"role": "assistant", "text": "..."}}
{"type": "status", "data": {"thinking": false}}
```

## Интеграция с React

В `client` можно добавить:

```ts
const ws = new WebSocket("ws://localhost:8765/ws");
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  if (msg.type === "chat") {
    // добавить сообщение в UI
  }
};
ws.send(JSON.stringify({ type: "chat", message: "Привет" }));
```

Связка с `AvatarPresence`: при `thinking: true` / `speaking: true` передавать пропсы.
