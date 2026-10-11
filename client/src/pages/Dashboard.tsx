import { useEffect, useState } from "react";

/**
 * IDA Retrowave Dashboard (React)
 * Full animated scene lives in /dashboard.html via Unified API.
 */
export default function Dashboard() {
  const [pulse, setPulse] = useState(true);
  const [clock, setClock] = useState("--:--:--");

  useEffect(() => {
    const a = setInterval(() => setPulse((p) => !p), 900);
    const b = setInterval(() => {
      setClock(new Date().toLocaleTimeString("ru-RU", { hour12: false }));
    }, 1000);
    return () => {
      clearInterval(a);
      clearInterval(b);
    };
  }, []);

  return (
    <div
      className="relative min-h-[70vh] overflow-hidden rounded-sm border border-pink-500/40 p-6"
      style={{
        fontFamily: "Orbitron, Share Tech Mono, monospace",
        background:
          "radial-gradient(ellipse at 50% 0%, rgba(123,44,191,0.35), transparent 55%), linear-gradient(180deg, #0a0014, #1a0033 60%, #2a0a1a)",
      }}
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px)",
        }}
      />
      <div className="relative z-10 space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h1
            className="text-2xl font-bold tracking-[0.15em]"
            style={{
              background: "linear-gradient(90deg, #00f0ff, #ff2bd6, #ffe66d)",
              WebkitBackgroundClip: "text",
              color: "transparent",
            }}
          >
            IDA RETROWAVE
          </h1>
          <div className="flex items-center gap-2 text-xs text-cyan-300">
            <span
              className={`inline-block h-2 w-2 rounded-full ${pulse ? "bg-green-400 shadow-[0_0_8px_#4ade80]" : "bg-green-400/40"}`}
            />
            ONLINE · {clock}
          </div>
        </div>

        <p className="text-sm text-fuchsia-200/80 tracking-wide">
          Полный анимированный дашборд (солнце, сетка, чат, аватар) —
          открой{" "}
          <a className="text-cyan-300 underline" href="/dashboard" target="_blank" rel="noreferrer">
            /dashboard
          </a>{" "}
          на Unified API (:8000).
        </p>

        <div className="grid gap-4 sm:grid-cols-3">
          {[
            { label: "NEURAL LINK", value: "ACTIVE", color: "#00f0ff" },
            { label: "JARVIS MODE", value: "ON", color: "#ff2bd6" },
            { label: "AVATAR", value: "IDLE", color: "#ffe66d" },
          ].map((c) => (
            <div
              key={c.label}
              className="border p-4"
              style={{
                borderColor: `${c.color}55`,
                boxShadow: `0 0 16px ${c.color}22`,
                background: "rgba(10,0,20,0.6)",
              }}
            >
              <div className="text-[10px] tracking-[0.2em]" style={{ color: c.color }}>
                {c.label}
              </div>
              <div className="mt-1 text-xl font-semibold text-white" style={{ textShadow: `0 0 10px ${c.color}` }}>
                {c.value}
              </div>
            </div>
          ))}
        </div>

        <div
          className="h-24 border border-cyan-500/30"
          style={{
            background:
              "repeating-linear-gradient(90deg, transparent, transparent 24px, rgba(0,240,255,0.15) 24px, rgba(0,240,255,0.15) 25px), repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(255,43,214,0.12) 24px, rgba(255,43,214,0.12) 25px)",
            transform: "perspective(200px) rotateX(12deg)",
            transformOrigin: "center bottom",
          }}
        />
      </div>
    </div>
  );
}
