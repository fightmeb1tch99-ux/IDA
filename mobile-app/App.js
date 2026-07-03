import React, { useState, useRef, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  FlatList,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

const COLORS = {
  primary: '#0a7ea4',
  background: '#151718',
  surface: '#1e2022',
  foreground: '#ECEDEE',
  muted: '#9BA1A6',
  border: '#334155',
};

export default function App() {
  const [messages, setMessages] = useState([
    {
      id: '1',
      content: 'Привет! Я IDA - Инновационный динамический помощник v 0.1. Чем я могу тебе помочь? 🤖',
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const flatListRef = useRef(null);

  useEffect(() => {
    flatListRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      content: inputText,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // ДОБАВЬ СВОЙ OPENAI API КЛЮЧ ЗДЕСЬ
      const OPENAI_API_KEY = 'sk-proj-...'; // Замени на свой ключ

      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${OPENAI_API_KEY}`,
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'system',
              content: 'Ты IDA - Инновационный динамический помощник v 0.1 - умный AI ассистент. Отвечай на русском языке кратко и дружелюбно.',
            },
            {
              role: 'user',
              content: inputText,
            },
          ],
          temperature: 0.7,
          max_tokens: 500,
        }),
      });

      const data = await response.json();

      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        content: data.choices?.[0]?.message?.content || 'Извини, произошла ошибка 😞',
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content: 'Ошибка подключения к OpenAI 😞',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const renderMessage = ({ item }) => {
    const isUser = item.role === 'user';
    return (
      <View
        style={[
          styles.messageContainer,
          isUser ? styles.userMessageContainer : styles.assistantMessageContainer,
        ]}
      >
        <View
          style={[
            styles.messageBubble,
            isUser ? styles.userBubble : styles.assistantBubble,
          ]}
        >
          <Text
            style={[
              styles.messageText,
              isUser ? styles.userText : styles.assistantText,
            ]}
          >
            {item.content}
          </Text>
          <Text style={styles.timestamp}>
            {item.timestamp.toLocaleTimeString('ru-RU', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>IDA - Инновационный динамический помощник v 0.1</Text>
          <Text style={styles.headerSubtitle}>🤖 AI Assistant</Text>
        </View>

        {/* Messages List */}
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderMessage}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.messagesList}
          onEndReachedThreshold={0.1}
        />

        {/* Input Area */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Напиши сообщение..."
            placeholderTextColor={COLORS.muted}
            value={inputText}
            onChangeText={setInputText}
            editable={!isLoading}
            multiline
            maxLength={1000}
          />
          <TouchableOpacity
            style={[
              styles.sendButton,
              (isLoading || !inputText.trim()) && styles.sendButtonDisabled,
            ]}
            onPress={handleSendMessage}
            disabled={isLoading || !inputText.trim()}
          >
            {isLoading ? (
              <ActivityIndicator size="small" color={COLORS.background} />
            ) : (
              <MaterialIcons name="send" size={20} color={COLORS.background} />
            )}
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  keyboardView: {
    flex: 1,
  },
  header: {
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: COLORS.background,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.foreground,
  },
  headerSubtitle: {
    fontSize: 12,
    color: COLORS.muted,
    marginTop: 4,
  },
  messagesList: {
    flexGrow: 1,
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
  userBubble: {
    backgroundColor: COLORS.primary,
  },
  assistantBubble: {
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: COLORS.background,
  },
  assistantText: {
    color: COLORS.foreground,
  },
  timestamp: {
    fontSize: 11,
    marginTop: 4,
    color: COLORS.muted,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    backgroundColor: COLORS.background,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  input: {
    flex: 1,
    borderRadius: 20,
    backgroundColor: COLORS.surface,
    paddingHorizontal: 16,
    paddingVertical: 10,
    color: COLORS.foreground,
    borderWidth: 1,
    borderColor: COLORS.border,
    maxHeight: 100,
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
});
