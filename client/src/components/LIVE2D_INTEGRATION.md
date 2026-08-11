# Live2D Integration for IDA (Mobile-ready)

## Dependencies

```bash
pnpm add pixi.js@^7 pixi-live2d-display
```

## Usage

```tsx
import Live2DAvatar from "@/components/Live2DAvatar";

<Live2DAvatar
  modelPath="/live2d/ida/ida.model3.json"
  isSpeaking={isSpeaking}
  isListening={isListening}
  width={280}
  height={380}
  interactive={true}
/>
```

## Mobile features

- Automatic responsive sizing (`window.innerWidth < 768`)
- Lower resolution & disabled antialiasing on mobile for better performance
- `powerPreference: "low-power"` on mobile
- Touch / tap interaction (plays "Tap" motion)
- `touch-action: manipulation` to avoid 300ms delay
- Graceful fallback text when model is not yet ready

## Current status

- Scaffold is in `public/live2d/ida/`
- Real `.moc3` + texture still needed
- Until the real model appears the component shows a soft fallback

## Next steps

1. Create the model in Live2D Cubism Editor
2. Export runtime files into `client/public/live2d/ida/`
3. Replace old `AvatarPresence` with `Live2DAvatar` in Chat / Dashboard pages
