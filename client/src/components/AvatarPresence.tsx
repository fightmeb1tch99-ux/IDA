import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

interface AvatarPresenceProps {
  isSpeaking?: boolean;
  isListening?: boolean;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

/**
 * Simple visual presence for IDA — first step towards a full Live2D / VRM avatar.
 * Cyberpunk style, animated when speaking or listening.
 */
export default function AvatarPresence({
  isSpeaking = false,
  isListening = false,
  className,
  size = 'md',
}: AvatarPresenceProps) {
  const [pulse, setPulse] = useState(0);

  useEffect(() => {
    if (!isSpeaking && !isListening) return;
    const id = setInterval(() => setPulse((p) => p + 1), 80);
    return () => clearInterval(id);
  }, [isSpeaking, isListening]);

  const sizeMap = {
    sm: 'w-16 h-16',
    md: 'w-28 h-28',
    lg: 'w-40 h-40',
  };

  const active = isSpeaking || isListening;

  return (
    <div className={cn('relative flex items-center justify-center', className)}>
      {/* Outer glow rings */}
      <div
        className={cn(
          'absolute rounded-full border transition-all duration-300',
          sizeMap[size],
          active
            ? 'border-cyan-400/40 scale-110 animate-pulse'
            : 'border-cyan-900/30 scale-100'
        )}
      />
      <div
        className={cn(
          'absolute rounded-full border transition-all duration-500',
          size === 'sm' ? 'w-20 h-20' : size === 'md' ? 'w-36 h-36' : 'w-52 h-52',
          active ? 'border-cyan-500/20 scale-105' : 'border-transparent'
        )}
      />

      {/* Core circle */}
      <div
        className={cn(
          'relative rounded-full flex items-center justify-center overflow-hidden',
          sizeMap[size],
          'bg-gradient-to-br from-slate-900 via-cyan-950 to-slate-900',
          'border-2',
          active ? 'border-cyan-400 shadow-[0_0_30px_rgba(34,211,238,0.4)]' : 'border-cyan-800/60'
        )}
      >
        {/* Inner IDA glyph */}
        <div className="relative z-10 select-none">
          <span
            className={cn(
              'font-bold tracking-wider text-cyan-300',
              size === 'sm' ? 'text-lg' : size === 'md' ? 'text-2xl' : 'text-4xl',
              active && 'animate-pulse'
            )}
          >
            IDA
          </span>
        </div>

        {/* Speaking bars */}
        {isSpeaking && (
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-0.5 items-end h-4">
            {[0, 1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="w-1 bg-cyan-400 rounded-full transition-all duration-75"
                style={{
                  height: `${4 + Math.sin(pulse * 0.4 + i) * 8 + 6}px`,
                }}
              />
            ))}
          </div>
        )}

        {/* Listening indicator */}
        {isListening && !isSpeaking && (
          <div className="absolute top-2 right-2 w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
        )}
      </div>

      {/* Status label */}
      <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[10px] uppercase tracking-widest text-cyan-600/80 whitespace-nowrap">
        {isSpeaking ? 'говорит' : isListening ? 'слушает' : 'онлайн'}
      </div>
    </div>
  );
}
```
