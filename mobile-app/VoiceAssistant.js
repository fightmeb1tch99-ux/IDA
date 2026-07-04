import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Animated,
  Easing,
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

export default function VoiceAssistant({ onVoiceInput }) {
  const [isListening, setIsListening] = useState(false);
  const [animationValue] = useState(new Animated.Value(0));
  const [waveAnimations] = useState([
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
    new Animated.Value(0),
  ]);

  useEffect(() => {
    if (isListening) {
      startWaveAnimation();
    } else {
      stopWaveAnimation();
    }
  }, [isListening]);

  const startWaveAnimation = () => {
    waveAnimations.forEach((anim, index) => {
      Animated.loop(
        Animated.sequence([
          Animated.timing(anim, {
            toValue: 1,
            duration: 600,
            delay: index * 100,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: false,
          }),
          Animated.timing(anim, {
            toValue: 0,
            duration: 600,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: false,
          }),
        ])
      ).start();
    });
  };

  const stopWaveAnimation = () => {
    waveAnimations.forEach((anim) => {
      anim.setValue(0);
    });
  };

  const handleMicPress = () => {
    setIsListening(!isListening);
    if (!isListening) {
      // Simulate voice input
      setTimeout(() => {
        onVoiceInput('Привет IDA');
        setIsListening(false);
      }, 2000);
    }
  };

  const waveScales = waveAnimations.map((anim) =>
    anim.interpolate({
      inputRange: [0, 1],
      outputRange: [1, 1.5],
    })
  );

  const waveOpacities = waveAnimations.map((anim) =>
    anim.interpolate({
      inputRange: [0, 1],
      outputRange: [1, 0],
    })
  );

  return (
    <View style={styles.container}>
      {/* Animated Avatar */}
      <View style={styles.avatarContainer}>
        {/* Wave Animation */}
        {waveScales.map((scale, index) => (
          <Animated.View
            key={`wave-${index}`}
            style={[
              styles.wave,
              {
                transform: [{ scale }],
                opacity: waveOpacities[index],
              },
            ]}
          />
        ))}

        {/* Avatar Circle */}
        <View style={styles.avatar}>
          <MaterialIcons name="mic" size={40} color={COLORS.foreground} />
        </View>
      </View>

      {/* Status Text */}
      <Text style={styles.statusText}>
        {isListening ? 'Слушаю...' : 'Нажми микрофон'}
      </Text>

      {/* Mic Button */}
      <TouchableOpacity
        style={[styles.micButton, isListening && styles.micButtonActive]}
        onPress={handleMicPress}
      >
        <MaterialIcons
          name={isListening ? 'mic' : 'mic-none'}
          size={32}
          color={COLORS.background}
        />
      </TouchableOpacity>

      {/* Info Text */}
      <Text style={styles.infoText}>
        {isListening
          ? 'Говори что-нибудь...'
          : 'Нажми кнопку и говори'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
    backgroundColor: COLORS.background,
  },
  avatarContainer: {
    width: 150,
    height: 150,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  wave: {
    position: 'absolute',
    width: 150,
    height: 150,
    borderRadius: 75,
    borderWidth: 2,
    borderColor: COLORS.primary,
  },
  avatar: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
  },
  statusText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.foreground,
    marginBottom: 20,
  },
  micButton: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  micButtonActive: {
    backgroundColor: '#ff6b6b',
  },
  infoText: {
    fontSize: 14,
    color: COLORS.muted,
    marginTop: 10,
  },
});
