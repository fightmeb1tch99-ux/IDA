"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { Application, Ticker, settings, RENDERER_TYPE } from "pixi.js";
import { Live2DModel } from "pixi-live2d-display/cubism4";
import { cn } from "@/lib/utils";

interface Live2DAvatarProps {
  modelPath?: string;
  isSpeaking?: boolean;
  isListening?: boolean;
  className?: string;
  width?: number;
  height?: number;
  interactive?: boolean;
  /** Max FPS (default 30 to save GPU/memory) */
  maxFPS?: number;
  /** Force low quality even on desktop */
  lowQuality?: boolean;
}

/**
 * Heavily optimized Live2D avatar for low memory & GPU usage.
 * Works well on both mobile and desktop.
 */
export default function Live2DAvatar({
  modelPath = "/live2d/ida/ida.model3.json",
  isSpeaking = false,
  isListening = false,
  className = "",
  width = 280,
  height = 380,
  interactive = true,
  maxFPS = 30,
  lowQuality = false,
}: Live2DAvatarProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const appRef = useRef<Application | null>(null);
  const modelRef = useRef<Live2DModel | null>(null);
  const loadedRef = useRef(false);
  const [isMobile, setIsMobile] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [actualSize, setActualSize] = useState({ w: width, h: height });

  // Detect device + responsive size
  useEffect(() => {
    const check = () => {
      const mobile =
        window.innerWidth < 768 ||
        "ontouchstart" in window ||
        navigator.maxTouchPoints > 0;
      setIsMobile(mobile);

      if (mobile && containerRef.current) {
        const maxW = Math.min(window.innerWidth * 0.65, 240);
        const ratio = height / width;
        setActualSize({ w: Math.round(maxW), h: Math.round(maxW * ratio) });
      } else {
        // Desktop: slightly smaller by default to save memory
        const scale = lowQuality ? 0.85 : 1;
        setActualSize({
          w: Math.round(width * scale),
          h: Math.round(height * scale),
        });
      }
    };

    check();
    window.addEventListener("resize", check, { passive: true });
    return () => window.removeEventListener("resize", check);
  }, [width, height, lowQuality]);

  // Init Pixi with aggressive memory optimizations
  useEffect(() => {
    if (!canvasRef.current) return;

    let destroyed = false;
    const { w, h } = actualSize;
    const useLow = isMobile || lowQuality;

    // Global Pixi settings for lower memory
    settings.RETINA_PREFIX = /@([0-9\.]+)x/;
    // @ts-ignore
    settings.FAIL_IF_MAJOR_PERFORMANCE_CAVEAT = false;

    const app = new Application({
      view: canvasRef.current,
      width: w,
      height: h,
      backgroundAlpha: 0,
      antialias: false,                    // always off → big memory & GPU save
      resolution: useLow ? 1 : Math.min(window.devicePixelRatio || 1, 1.5),
      autoDensity: true,
      powerPreference: "low-power",        // prefer integrated GPU
      preserveDrawingBuffer: false,
      clearBeforeRender: true,
      hello: false,
    });

    // Limit FPS
    app.ticker.maxFPS = maxFPS;
    app.ticker.minFPS = 20;

    // Stop ticker when tab is hidden (huge memory/CPU save)
    const onVisibility = () => {
      if (document.hidden) {
        app.ticker.stop();
      } else {
        app.ticker.start();
      }
    };
    document.addEventListener("visibilitychange", onVisibility);

    appRef.current = app;

    (async () => {
      try {
        const model = await Live2DModel.from(modelPath, {
          ticker: Ticker.shared,
          // Reduce internal buffers if possible
        });

        if (destroyed) {
          model.destroy();
          return;
        }

        const scale = Math.min(w / model.width, h / model.height) * 0.9;
        model.scale.set(scale);
        model.x = w / 2;
        model.y = h * 0.95;
        model.anchor.set(0.5, 1);

        // Disable expensive features when possible
        if (model.internalModel) {
          // Reduce physics update rate on low-end
          try {
            // @ts-ignore
            if (model.internalModel.physics) {
              // physics still runs but we throttle via low FPS
            }
          } catch {}
        }

        if (interactive) {
          model.interactive = true;
          model.cursor = "pointer";
          model.on("pointertap", () => {
            model.motion("Tap").catch(() => {
              model.motion("Idle").catch(() => {});
            });
          });
        }

        app.stage.addChild(model);
        modelRef.current = model;
        loadedRef.current = true;
        setLoadError(false);

        // Start with idle, but only once
        model.motion("Idle").catch(() => {});
      } catch (err) {
        console.warn("[Live2DAvatar] Model not ready:", err);
        loadedRef.current = false;
        setLoadError(true);
      }
    })();

    return () => {
      destroyed = true;
      document.removeEventListener("visibilitychange", onVisibility);

      if (modelRef.current) {
        try {
          modelRef.current.destroy({ children: true, texture: false, baseTexture: false });
        } catch {}
        modelRef.current = null;
      }

      if (appRef.current) {
        appRef.current.destroy(true, { children: true, texture: false, baseTexture: false });
        appRef.current = null;
      }

      loadedRef.current = false;
    };
  }, [modelPath, actualSize.w, actualSize.h, isMobile, interactive, maxFPS, lowQuality]);

  // Speaking / Listening
  useEffect(() => {
    const model = modelRef.current;
    if (!model || !loadedRef.current) return;

    const play = (group: string) => {
      model.motion(group).catch(() => {});
    };

    if (isSpeaking) play("Talk");
    else if (isListening) play("Listen");
    else play("Idle");
  }, [isSpeaking, isListening]);

  const handleTap = useCallback(() => {
    const model = modelRef.current;
    if (!model || !loadedRef.current) return;
    model.motion("Tap").catch(() => model.motion("Idle").catch(() => {}));
  }, []);

  return (
    <div
      ref={containerRef}
      className={cn(
        "relative flex flex-col items-center justify-center select-none",
        className
      )}
      onClick={interactive ? handleTap : undefined}
    >
      <canvas
        ref={canvasRef}
        style={{
          width: actualSize.w,
          height: actualSize.h,
          display: "block",
          maxWidth: "100%",
          touchAction: "manipulation",
          // Promote to own layer but keep memory low
          willChange: "auto",
        }}
        className="rounded-xl"
      />

      <div className="mt-1 text-[10px] uppercase tracking-widest text-cyan-600/80 whitespace-nowrap">
        {isSpeaking ? "говорит" : isListening ? "слушает" : "онлайн"}
      </div>

      {loadError && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center text-cyan-700/60 text-xs px-4">
            <div className="font-bold text-lg mb-1">IDA</div>
            <div>модель загружается…</div>
          </div>
        </div>
      )}
    </div>
  );
}
