import React, { useState } from 'react';
import { View, TouchableOpacity, Text, StyleSheet, useColorScheme } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

interface VoiceAssistantProps {
  onVoiceInput: (text: string) => void;
}

export default function VoiceAssistant({ onVoiceInput }: VoiceAssistantProps) {
  const colorScheme = useColorScheme();
  const [isListening, setIsListening] = useState(false);

  const LIGHT_COLORS = {
    background: '#ffffff',
    surface: '#f5f5f5',
    foreground: '#1a1a1a',
    primary: '#3b82f6',
    muted: '#9ca3af',
  };

  const DARK_COLORS = {
    background: '#0a0e1a',
    surface: '#111827',
    foreground: '#f1f5f9',
    primary: '#3b82f6',
    muted: '#94a3b8',
  };

  const COLORS = colorScheme === 'dark' ? DARK_COLORS : LIGHT_COLORS;

  const handleStartListening = () => {
    setIsListening(true);
    // TODO: Integrate with Whisper API or native speech recognition
    setTimeout(() => {
      setIsListening(false);
      onVoiceInput('Пример голосового ввода');
    }, 2000);
  };

  return (
    <View style={[styles.container, { backgroundColor: COLORS.surface }]}>
      <MaterialIcons name="mic" size={48} color={COLORS.primary} />
      <Text style={[styles.title, { color: COLORS.foreground }]}>
        {isListening ? 'Слушаю...' : 'Нажми для голосового ввода'}
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
        <MaterialIcons
          name={isListening ? 'stop' : 'mic'}
          size={32}
          color="#fff"
        />
      </TouchableOpacity>
      <Text style={[styles.subtitle, { color: COLORS.muted }]}>
        Голосовой помощник в разработке
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
  title: {
    fontSize: 16,
    fontWeight: '600',
    marginTop: 12,
  },
  button: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginVertical: 20,
  },
  buttonActive: {
    opacity: 0.7,
  },
  subtitle: {
    fontSize: 12,
    marginTop: 8,
  },
});
