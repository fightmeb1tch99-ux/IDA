# Live2D Integration for IDA (Memory-optimized)

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
  maxFPS={30}          // lower = less GPU/memory
  lowQuality={false}   // true = even more aggressive
  interactive={true}
/>
```

## Optimizations applied (all devices)

- Antialiasing **disabled** everywhere
- Resolution capped (1× on mobile / lowQuality, max 1.5× on desktop)
- `powerPreference: "low-power"`
- FPS limited (default 30)
- Ticker **stops** when tab is hidden
- Smaller default size on desktop
- Proper destroy of model + app (no texture leaks)
- `touch-action: manipulation`
- Passive resize listener

## Current status

- Scaffold in `public/live2d/ida/`
- Real `.moc3` + texture still required
- Until then the component shows a soft fallback

## Next steps

1. Create model in Live2D Cubism Editor
2. Export into `client/public/live2d/ida/`
3. Replace `AvatarPresence` with `Live2DAvatar`
