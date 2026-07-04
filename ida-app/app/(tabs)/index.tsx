import React, { useState, useRef, useEffect } from 'react';
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

// Color scheme
const LIGHT_COLORS = {
  background: '#ffffff',
  surface: '#f5f5f5',
  foreground: '#1a1a1a',
  primary: '#3b82f6',
  muted: '#9ca3af',
  border: '#e5e7eb',
};

const DARK_COLORS = {
  background: '#0a0e1a',
  surface: '#111827',
  foreground: '#f1f5f9',
  primary: '#3b82f6',
  muted: '#94a3b8',
  border: 'rgba(148,163,184,0.12)',
};

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

export default function ChatScreen() {
  const colorScheme = useColorScheme();
  const COLORS = colorScheme === 'dark' ? DARK_COLORS : LIGHT_COLORS;

  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Привет! Я IDA — твой персональный ассистент. Чем я могу помочь?',
      sender: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showVoiceModal, setShowVoiceModal] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(colorScheme === 'dark');
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Call IDA backend API
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputText }),
      });

      if (!response.ok) throw new Error('API error');
      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response || 'Извини, я не смог обработать твой запрос.',
        sender: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Ошибка подключения. Проверь, запущен ли IDA сервер.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceInput = (voiceText: string) => {
    setInputText(voiceText);
    setShowVoiceModal(false);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: COLORS.background }]}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        {/* Header */}
        <View style={[styles.header, { borderBottomColor: COLORS.border, backgroundColor: COLORS.background }]}>
          <View style={styles.headerTop}>
            <View>
              <Text style={[styles.headerTitle, { color: COLORS.foreground }]}>IDA</Text>
              <Text style={[styles.headerSubtitle, { color: COLORS.muted }]}>Инновационный помощник</Text>
            </View>
            <TouchableOpacity
              style={styles.themeButton}
              onPress={() => setIsDarkMode(!isDarkMode)}
            >
              <MaterialIcons
                name={isDarkMode ? 'light-mode' : 'dark-mode'}
                size={24}
                color={COLORS.primary}
              />
            </TouchableOpacity>
          </View>
        </View>

        {/* Messages List */}
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesList}
          contentContainerStyle={{ flexGrow: 1, justifyContent: 'flex-end' }}
        >
          {messages.map((message) => (
            <View
              key={message.id}
              style={[
                styles.messageContainer,
                message.sender === 'user'
                  ? styles.userMessageContainer
                  : styles.assistantMessageContainer,
              ]}
            >
              <View
                style={[
                  styles.messageBubble,
                  message.sender === 'user'
                    ? [styles.userBubble, { backgroundColor: COLORS.primary }]
                    : [styles.assistantBubble, { backgroundColor: COLORS.surface, borderColor: COLORS.border }],
                ]}
              >
                <Text
                  style={[
                    styles.messageText,
                    message.sender === 'user'
                      ? [styles.userText, { color: '#fff' }]
                      : [styles.assistantText, { color: COLORS.foreground }],
                  ]}
                >
                  {message.text}
                </Text>
                <Text
                  style={[
                    styles.timestamp,
                    { color: COLORS.muted },
                  ]}
                >
                  {formatTime(message.timestamp)}
                </Text>
              </View>
            </View>
          ))}
          {isLoading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color={COLORS.primary} />
              <Text style={[styles.loadingText, { color: COLORS.muted }]}>IDA думает...</Text>
            </View>
          )}
        </ScrollView>

        {/* Input Area */}
        <View style={[styles.inputContainer, { borderTopColor: COLORS.border, backgroundColor: COLORS.background }]}>
          <TextInput
            style={[
              styles.input,
              {
                backgroundColor: COLORS.surface,
                color: COLORS.foreground,
                borderColor: COLORS.border,
              },
            ]}
            placeholder="Напиши сообщение..."
            placeholderTextColor={COLORS.muted}
            value={inputText}
            onChangeText={setInputText}
            editable={!isLoading}
            multiline
            maxLength={1000}
          />
          <TouchableOpacity
            style={[styles.voiceButton, { backgroundColor: COLORS.muted }]}
            onPress={() => setShowVoiceModal(true)}
          >
            <MaterialIcons name="mic" size={20} color={COLORS.background} />
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.sendButton,
              { backgroundColor: COLORS.primary },
              (isLoading || !inputText.trim()) && styles.sendButtonDisabled,
            ]}
            onPress={handleSendMessage}
            disabled={isLoading || !inputText.trim()}
          >
            {isLoading ? (
              <ActivityIndicator size="small" color="#fff" />
            ) : (
              <MaterialIcons name="send" size={20} color="#fff" />
            )}
          </TouchableOpacity>
        </View>

        {/* Voice Modal */}
        <Modal
          visible={showVoiceModal}
          transparent={true}
          animationType="fade"
          onRequestClose={() => setShowVoiceModal(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={[styles.modalContent, { backgroundColor: COLORS.background, borderColor: COLORS.border }]}>
              <Text style={[{ color: COLORS.foreground, fontSize: 16, fontWeight: '600' }]}>🎤 Голосовой ввод</Text>
              <Text style={[{ color: COLORS.muted, marginTop: 8, textAlign: 'center' }]}>Скоро будет интегрирован голосовой помощник</Text>
              <TouchableOpacity
                style={[styles.closeButton, { backgroundColor: COLORS.primary }]}
                onPress={() => setShowVoiceModal(false)}
              >
                <Text style={styles.closeButtonText}>Закрыть</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  header: {
    borderBottomWidth: 1,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  themeButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    fontSize: 12,
    marginTop: 4,
  },
  messagesList: {
    flex: 1,
    paddingHorizontal: 12,
    paddingVertical: 12,
  },
  messageContainer: {
    marginVertical: 6,
    flexDirection: 'row',
  },
  userMessageContainer: {
    justifyContent: 'flex-end',
  },
  assistantMessageContainer: {
    justifyContent: 'flex-start',
  },
  messageBubble: {
    maxWidth: '80%',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  userBubble: {},
  assistantBubble: {
    borderWidth: 1,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {},
  assistantText: {},
  timestamp: {
    fontSize: 11,
    marginTop: 4,
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 20,
  },
  loadingText: {
    marginTop: 10,
    fontSize: 14,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    borderTopWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  input: {
    flex: 1,
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderWidth: 1,
    maxHeight: 100,
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
  voiceButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 4,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: '90%',
    borderRadius: 20,
    padding: 20,
    alignItems: 'center',
    borderWidth: 1,
  },
  closeButton: {
    marginTop: 20,
    paddingHorizontal: 30,
    paddingVertical: 10,
    borderRadius: 8,
  },
  closeButtonText: {
    color: '#fff',
    fontWeight: '600',
  },
});
