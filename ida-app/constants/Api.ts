/**
 * IDA backend for Android / iOS.
 * На телефоне — IP компа в одной Wi‑Fi сети.
 * EXPO_PUBLIC_API_URL=http://192.168.1.10:8000
 */
const host = (process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

export const API_BASE = host;
export const WS_URL = process.env.EXPO_PUBLIC_WS_URL || host.replace(/^http/, "ws") + "/ws";
export const CHAT_URL = `${API_BASE}/api/chat`;
export const HEALTH_URL = `${API_BASE}/health`;
export const PROFILE_URL = `${API_BASE}/api/profile`;
