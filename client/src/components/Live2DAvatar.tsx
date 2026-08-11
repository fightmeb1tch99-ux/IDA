"use client";

import { useEffect, useRef } from "react";
import { Application, Ticker } from "pixi.js";
import { Live2DModel } from "pixi-live2d-display/cubism4";
import { cn } from "@/lib/utils";

interface Live2DAvatarProps {
  /** Path to .model3.json */
  modelPath?: string;
  isSpeaking?: boolean;
  isListening?: boolean;
  className?: string;
  width?: number;
  height?: number;
  /** Fallback to simple AvatarPresence style when model fails to load */
  showFallback?: boolean;
}

/**
 * Live2D avatar component for IDA.
 * Requires a valid Cubism model at modelPath.
 * Falls back gracefully if the model is not yet ready.
 */
export default function Live2DAvatar({
  modelPath = "/live2d/ida/ida.model3.json",
  isSpeaking = false,
  isListening = false,
  className = "",
  width = 280,
  height = 380,
  showFallback = true,
}: Live2DAvatarProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const appRef = useRef<Application | null>(null);
  const modelRef = useRef<Live2DModel | null>(null);
  const loadedRef = useRef(false);

  useEffect(() => {
    if (!canvasRef.current) return;

    let destroyed = false;

    const app = new Application({
      view: canvasRef.current,
      width,
      height,
      backgroundAlpha: 0,
      antialias: true,
      resolution: window.devicePixelRatio || 1,
      autoDensity: true,
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

        // Scale and position
        const scale = Math.min(width / model.width, height / model.height) * 0.9;
        model.scale.set(scale);
        model.x = width / 2;
        model.y = height * 0.95;
        model.anchor.set(0.5, 1);

        app.stage.addChild(model);
        modelRef.current = model;
        loadedRef.current = true;

        // Start idle
        model.motion("Idle").catch(() => {
          // motion may not exist yet
        });
      } catch (err) {
        console.warn("[Live2DAvatar] Model not ready yet:", err);
        loadedRef.current = false;
      }
    })();

    return () => {
      destroyed = true;
      if (appRef.current) {
        appRef.current.destroy(true, { children: true });
        appRef.current = null;
      }
      modelRef.current = null;
    };
  }, [modelPath, width, height]);

  // React to speaking / listening state
  useEffect(() => {
    const model = modelRef.current;
    if (!model || !loadedRef.current) return;

    const play = async (group: string) => {
      try {
        await model.motion(group);
      } catch {
        // ignore missing motion groups
      }
    };

    if (isSpeaking) {
      play("Talk");
    } else if (isListening) {
      play("Listen");
    } else {
      play("Idle");
    }
  }, [isSpeaking, isListening]);

  return (
    <div className={cn("relative flex items-center justify-center", className)}>
      <canvas
        ref={canvasRef}
        style={{ width, height, display: "block" }}
        className="rounded-lg"
      />
      {/* Optional status label */}
      <div className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[10px] uppercase tracking-widest text-cyan-600/80 whitespace-nowrap">
        {isSpeaking ? "говорит" : isListening ? "слушает" : "онлайн"}
      </div>
    </div>
  );
}
