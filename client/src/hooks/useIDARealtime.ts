import { useEffect, useRef, useState, useCallback } from "react";

export type RealtimeStatus = {
  connected: boolean;
  thinking: boolean;
  speaking: boolean;
};

export type RealtimeMessage = {
  role: "user" | "assistant";
  text: string;
};

type Options = {
  url?: string;
  onMessage?: (msg: RealtimeMessage) => void;
  enabled?: boolean;
};

/**
 * Hook to connect to IDA Realtime Bridge (realtime/bridge.py)
 * Default: ws://localhost:8765/ws
 */
export function useIDARealtime(options: Options = {}) {
  const {
    url = "ws://localhost:8765/ws",
    onMessage,
    enabled = true,
  } = options;

  const wsRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<RealtimeStatus>({
    connected: false,
    thinking: false,
    speaking: false,
  });
  const [lastError, setLastError] = useState<string | null>(null);
  const onMessageRef = useRef(onMessage);
  onMessageRef.current = onMessage;

  const connect = useCallback(() => {
    if (!enabled || typeof window === "undefined") return;
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;

      ws.onopen = () => {
        setStatus((s) => ({ ...s, connected: true }));
        setLastError(null);
      };

      ws.onclose = () => {
        setStatus({ connected: false, thinking: false, speaking: false });
        // auto-reconnect after 3s
        setTimeout(() => {
          if (enabled) connect();
        }, 3000);
      };

      ws.onerror = () => {
        setLastError("WebSocket error — is realtime/bridge.py running?");
      };

      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.type === "status" && msg.data) {
            setStatus((s) => ({
              ...s,
              thinking: !!msg.data.thinking,
              speaking: !!msg.data.speaking,
              connected: true,
            }));
          }
          if (msg.type === "chat" && msg.data?.text) {
            onMessageRef.current?.({
              role: msg.data.role || "assistant",
              text: msg.data.text,
            });
            setStatus((s) => ({ ...s, thinking: false, speaking: false }));
          }
        } catch {
          // ignore non-json
        }
      };
    } catch (e) {
      setLastError(String(e));
    }
  }, [url, enabled]);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
      wsRef.current = null;
    };
  }, [connect]);

  const send = useCallback((message: string) => {
    if (!message.trim()) return false;
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setLastError("Not connected to IDA bridge");
      return false;
    }
    ws.send(JSON.stringify({ type: "chat", message }));
    setStatus((s) => ({ ...s, thinking: true }));
    return true;
  }, []);

  return { status, send, lastError, reconnect: connect };
}
