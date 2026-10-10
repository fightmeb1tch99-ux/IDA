import React, { useState } from 'react';
import { View, TouchableOpacity, StyleSheet, Platform } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { Text } from '@/components/Themed';

type Colors = {
  surface: string;
  foreground: string;
  primary: string;
  muted: string;
};

type Props = {
  onVoiceInput: (text: string) => void;
  colors?: Colors;
};

/**
 * Голосовой ввод для Android / iOS.
 * Нативное распознавание подключается через expo-speech / Whisper позже.
 * Сейчас: быстрый ручной ввод-фолбэк + хук под native STT.
 */
export default function VoiceAssistant({ onVoiceInput, colors }: Props) {
  const COLORS = colors || {
    surface: '#111827',
    foreground: '#f1f5f9',
    primary: '#3b82f6',
    muted: '#94a3b8',
  };
  const [isListening, setIsListening] = useState(false);

  const handleStartListening = () => {
    setIsListening(true);
    // Плейсхолдер: на проде — expo-av + Whisper / native Speech Recognition
    setTimeout(() => {
      setIsListening(false);
      const sample =
        Platform.OS === 'ios'
          ? 'Привет IDA, что ты умеешь?'
          : 'Привет IDA, какая погода?';
      onVoiceInput(sample);
    }, 1500);
  };

  return (
    <View style={[styles.container, { backgroundColor: COLORS.surface }]}>
      <MaterialIcons name="mic" size={48} color={COLORS.primary} />
      <Text style={[styles.title, { color: COLORS.foreground }]}>
        {isListening ? 'Слушаю…' : 'Нажми — сказать IDA'}
      </Text>
      <TouchableOpacity
        style={[
          styles.button,
          { backgroundColor: COLORS.primary },
          isListening && styles.buttonActive,
        ]}
        onPress={handleStartListening}
        disabled={isListening}
      >
        <MaterialIcons name={isListening ? 'stop' : 'mic'} size={32} color="#fff" />
      </TouchableOpacity>
      <Text style={[styles.subtitle, { color: COLORS.muted }]}>
        Android · iOS · голос → чат с аватаром-Джарвисом
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 20,
    borderRadius: 12,
  },
  title: { fontSize: 16, fontWeight: '600', marginTop: 12 },
  button: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 20,
  },
  buttonActive: { opacity: 0.7 },
  subtitle: { fontSize: 12, marginTop: 8, textAlign: 'center' },
});
