import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  StyleSheet,
  View,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  Modal,
  useColorScheme,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { Text } from '@/components/Themed';
import { API_BASE, CHAT_URL, HEALTH_URL, WS_URL } from '@/constants/Api';
import VoiceAssistant from '@/components/VoiceAssistant';

const LIGHT_COLORS = {
  background: '#ffffff',
  surface: '#f5f5f5',
  foreground: '#1a1a1a',
  primary: '#3b82f6',
  muted: '#9ca3af',
  border: '#e5e7eb',
  success: '#22c55e',
  danger: '#ef4444',
};

const DARK_COLORS = {
  background: '#0a0e1a',
  surface: '#111827',
  foreground: '#f1f5f9',
  primary: '#3b82f6',
  muted: '#94a3b8',
  border: 'rgba(148,163,184,0.12)',
  success: '#22c55e',
  danger: '#ef4444',
};

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

type ConnState = 'online' | 'offline' | 'checking';

export default function ChatScreen() {
  const colorScheme = useColorScheme();
  const COLORS = colorScheme === 'dark' ? DARK_COLORS : LIGHT_COLORS;

  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text:
        'Привет. Я IDA — твой компаньон в стиле Джарвиса. Пиши или говори: могу ответить, посчитать, запомнить, найти и подсказать следующий шаг.',
      sender: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showVoiceModal, setShowVoiceModal] = useState(false);
  const [conn, setConn] = useState<ConnState>('checking');
  const scrollViewRef = useRef<ScrollView>(null);

  const checkHealth = useCallback(async () => {
    setConn('checking');
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 4000);
      const r = await fetch(HEALTH_URL, { signal: ctrl.signal });
      clearTimeout(t);
      setConn(r.ok ? 'online' : 'offline');
    } catch {
      setConn('offline');
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const id = setInterval(checkHealth, 20000);
    return () => clearInterval(id);
  }, [checkHealth]);

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const sendToBackend = async (text: string): Promise<string> => {
    const response = await fetch(CHAT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    if (data.error) throw new Error(data.error);
    return data.response || 'Пустой ответ от IDA.';
  };

  const handleSendMessage = async (override?: string) => {
    const text = (override ?? inputText).trim();
    if (!text) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const reply = await sendToBackend(text);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          text: reply,
          sender: 'assistant',
          timestamp: new Date(),
        },
      ]);
      setConn('online');
    } catch (e: any) {
      setConn('offline');
      const hint =
        Platform.OS !== 'web'
          ? `\n\nНа телефоне укажи IP компьютера:\nEXPO_PUBLIC_API_URL=http://ВАШ_IP:8000\nСейчас: ${API_BASE}\nWS: ${WS_URL}`
          : '';
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          text: `Не достучался до сервера (${e?.message || e}). Запусти ./start.sh на ПК.${hint}`,
          sender: 'assistant',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const onVoiceInput = (text: string) => {
    setShowVoiceModal(false);
    if (text) handleSendMessage(text);
  };

  const statusColor =
    conn === 'online' ? COLORS.success : conn === 'checking' ? COLORS.muted : COLORS.danger;
  const statusLabel =
    conn === 'online' ? 'на связи' : conn === 'checking' ? 'проверка…' : 'нет связи';

  return (
    <SafeAreaView style={[styles.safe, { backgroundColor: COLORS.background }]}>
      <View style={[styles.header, { borderBottomColor: COLORS.border }]}>
        <View>
          <Text style={[styles.title, { color: COLORS.foreground }]}>IDA</Text>
          <Text style={[styles.sub, { color: COLORS.muted }]}>Джарвис-режим · смартфон</Text>
        </View>
        <TouchableOpacity onPress={checkHealth} style={styles.statusBtn}>
          <View style={[styles.dot, { backgroundColor: statusColor }]} />
          <Text style={{ color: COLORS.muted, fontSize: 12 }}>{statusLabel}</Text>
        </TouchableOpacity>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 8 : 0}
      >
        <ScrollView
          ref={scrollViewRef}
          style={styles.list}
          contentContainerStyle={{ padding: 16, paddingBottom: 24 }}
        >
          {messages.map((m) => (
            <View
              key={m.id}
              style={[
                styles.bubble,
                m.sender === 'user'
                  ? { alignSelf: 'flex-end', backgroundColor: COLORS.primary }
                  : { alignSelf: 'flex-start', backgroundColor: COLORS.surface },
              ]}
            >
              <Text
                style={{
                  color: m.sender === 'user' ? '#fff' : COLORS.foreground,
                  fontSize: 15,
                  lineHeight: 22,
                }}
              >
                {m.text}
              </Text>
            </View>
          ))}
          {isLoading && (
            <ActivityIndicator style={{ marginTop: 8 }} color={COLORS.primary} />
          )}
        </ScrollView>

        <View style={[styles.inputRow, { borderTopColor: COLORS.border, backgroundColor: COLORS.background }]}>
          <TouchableOpacity onPress={() => setShowVoiceModal(true)} style={styles.iconBtn}>
            <MaterialIcons name="mic" size={24} color={COLORS.primary} />
          </TouchableOpacity>
          <TextInput
            style={[
              styles.input,
              {
                backgroundColor: COLORS.surface,
                color: COLORS.foreground,
                borderColor: COLORS.border,
              },
            ]}
            placeholder="Скажи IDA…"
            placeholderTextColor={COLORS.muted}
            value={inputText}
            onChangeText={setInputText}
            onSubmitEditing={() => handleSendMessage()}
            returnKeyType="send"
          />
          <TouchableOpacity
            onPress={() => handleSendMessage()}
            style={[styles.send, { backgroundColor: COLORS.primary }]}
            disabled={isLoading}
          >
            <MaterialIcons name="send" size={20} color="#fff" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>

      <Modal visible={showVoiceModal} animationType="slide" transparent>
        <View style={styles.modalBg}>
          <View style={[styles.modalCard, { backgroundColor: COLORS.surface }]}>
            <VoiceAssistant onVoiceInput={onVoiceInput} colors={COLORS} />
            <TouchableOpacity onPress={() => setShowVoiceModal(false)}>
              <Text style={{ color: COLORS.primary, textAlign: 'center', marginTop: 12 }}>Закрыть</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1 },
  header: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
  },
  title: { fontSize: 20, fontWeight: '700' },
  sub: { fontSize: 12, marginTop: 2 },
  statusBtn: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  dot: { width: 8, height: 8, borderRadius: 4 },
  list: { flex: 1 },
  bubble: {
    maxWidth: '85%',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 16,
    marginBottom: 10,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 10,
    borderTopWidth: 1,
    gap: 8,
  },
  iconBtn: { padding: 6 },
  input: {
    flex: 1,
    borderWidth: 1,
    borderRadius: 20,
    paddingHorizontal: 14,
    paddingVertical: Platform.OS === 'ios' ? 10 : 8,
    fontSize: 15,
  },
  send: {
    width: 40,
    height: 40,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  modalBg: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalCard: {
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    padding: 20,
    paddingBottom: 36,
  },
});
