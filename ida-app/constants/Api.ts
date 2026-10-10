/**
 * IDA backend endpoints for Android / iOS.
 *
 * На телефоне localhost НЕ работает — укажи IP компа в одной сети Wi‑Fi.
 * Пример: EXPO_PUBLIC_API_URL=http://192.168.1.10:8000
 *          EXPO_PUBLIC_WS_URL=ws://192.168.1.10:8765/ws
 */
const host = process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000";
const wsHost = process.env.EXPO_PUBLIC_WS_URL || "ws://127.0.0.1:8765/ws";

export const API_BASE = host.replace(/\/$/, "");
export const WS_URL = wsHost;
export const CHAT_URL = `${API_BASE}/api/chat`;
export const HEALTH_URL = `${API_BASE}/health`;
