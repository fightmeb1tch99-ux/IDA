"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { Application, Ticker } from "pixi.js";
import { Live2DModel } from "pixi-live2d-display/cubism4";
import { cn } from "@/lib/utils";

interface Live2DAvatarProps {
  /** Path to .model3.json */
  modelPath?: string;
  isSpeaking?: boolean;
  isListening?: boolean;
  className?: string;
  /** Base width (will be scaled on mobile) */
  width?: number;
  /** Base height (will be scaled on mobile) */
  height?: number;
  /** Enable touch interaction (tap to play motion) */
  interactive?: boolean;
}

/**
 * Live2D avatar component for IDA — mobile-first.
 * - Responsive sizing
 * - Touch support
 * - Graceful fallback when model is not ready
 * - Performance-conscious on low-end devices
 */
export default function Live2DAvatar({
  modelPath = "/live2d/ida/ida.model3.json",
  isSpeaking = false,
  isListening = false,
  className = "",
  width = 280,
  height = 380,
  interactive = true,
}: Live2DAvatarProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const appRef = useRef<Application | null>(null);
  const modelRef = useRef<Live2DModel | null>(null);
  const loadedRef = useRef(false);
  const [isMobile, setIsMobile] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [actualSize, setActualSize] = useState({ w: width, h: height });

  // Detect mobile + compute responsive size
  useEffect(() => {
    const check = () => {
      const mobile = window.innerWidth < 768 || "ontouchstart" in window;
      setIsMobile(mobile);

      if (mobile && containerRef.current) {
        const maxW = Math.min(window.innerWidth * 0.7, 260);
        const ratio = height / width;
        setActualSize({ w: maxW, h: maxW * ratio });
      } else {
        setActualSize({ w: width, h: height });
      }
    };

    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, [width, height]);

  // Init Pixi + Live2D
  useEffect(() => {
    if (!canvasRef.current) return;

    let destroyed = false;
    const { w, h } = actualSize;

    const app = new Application({
      view: canvasRef.current,
      width: w,
      height: h,
      backgroundAlpha: 0,
      antialias: !isMobile, // disable AA on mobile for perf
      resolution: Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 2),
      autoDensity: true,
      powerPreference: isMobile ? "low-power" : "high-performance",
    });
    appRef.current = app;

    (async () => {
      try {
        const model = await Live2DModel.from(modelPath, {
          ticker: Ticker.shared,
        });

        if (destroyed) {
          model.destroy();
          return;
        }

        const scale = Math.min(w / model.width, h / model.height) * 0.92;
        model.scale.set(scale);
        model.x = w / 2;
        model.y = h * 0.96;
        model.anchor.set(0.5, 1);

        // Touch / click interaction
        if (interactive) {
          model.interactive = true;
          model.buttonMode = true;
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

        model.motion("Idle").catch(() => {});
      } catch (err) {
        console.warn("[Live2DAvatar] Model not ready:", err);
        loadedRef.current = false;
        setLoadError(true);
      }
    })();

    return () => {
      destroyed = true;
      if (appRef.current) {
        appRef.current.destroy(true, { children: true });
        appRef.current = null;
      }
      modelRef.current = null;
      loadedRef.current = false;
    };
  }, [modelPath, actualSize.w, actualSize.h, isMobile, interactive]);

  // Speaking / Listening state
  useEffect(() => {
    const model = modelRef.current;
    if (!model || !loadedRef.current) return;

    const play = (group: string) => {
      model.motion(group).catch(() => {});
    };

    if (isSpeaking) {
      play("Talk");
    } else if (isListening) {
      play("Listen");
    } else {
      play("Idle");
    }
  }, [isSpeaking, isListening]);

  const handleTap = useCallback(() => {
    const model = modelRef.current;
    if (!model || !loadedRef.current) return;
    model.motion("Tap").catch(() => {
      model.motion("Idle").catch(() => {});
    });
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
        }}
        className="rounded-xl"
      />

      {/* Status label */}
      <div className="mt-1 text-[10px] uppercase tracking-widest text-cyan-600/80 whitespace-nowrap">
        {isSpeaking ? "говорит" : isListening ? "слушает" : "онлайн"}
      </div>

      {/* Fallback when model is missing */}
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
