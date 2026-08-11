# Live2D Integration for IDA

## Dependencies

```bash
pnpm add pixi.js@^7 pixi-live2d-display
```

> Use pixi.js v7 for best compatibility with pixi-live2d-display.

## Usage

```tsx
import Live2DAvatar from "@/components/Live2DAvatar";

<Live2DAvatar
  modelPath="/live2d/ida/ida.model3.json"
  isSpeaking={isSpeaking}
  isListening={isListening}
  width={280}
  height={380}
/>
```

## Current status

- Scaffold is in `public/live2d/ida/`
- Real `.moc3` + texture still needed (create in Cubism Editor)
- Until the real model is ready the component will log a warning and show nothing (or you can keep the old AvatarPresence as fallback)

## Next steps

1. Create the model in Live2D Cubism Editor using the character references
2. Export runtime files into `client/public/live2d/ida/`
3. Replace AvatarPresence with Live2DAvatar in Chat / Dashboard
