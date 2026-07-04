import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

const COLORS = {
  primary: '#0a7ea4',
  surface: '#1e2022',
  foreground: '#ECEDEE',
  border: '#334155',
};

const QUICK_COMMANDS = [
  { icon: 'schedule', label: 'Время', command: 'Сколько сейчас времени?' },
  { icon: 'calendar-today', label: 'Дата', command: 'Какая сегодня дата?' },
  { icon: 'cloud', label: 'Погода', command: 'Как погода?' },
  { icon: 'newspaper', label: 'Новости', command: 'Расскажи новости' },
];

export default function QuickCommands({ onCommand }) {
  return (
    <View style={styles.container}>
      {QUICK_COMMANDS.map((cmd, index) => (
        <TouchableOpacity
          key={index}
          style={styles.button}
          onPress={() => onCommand(cmd.command)}
        >
          <MaterialIcons name={cmd.icon} size={20} color={COLORS.primary} />
          <Text style={styles.label}>{cmd.label}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 12,
    paddingVertical: 12,
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
  },
  button: {
    alignItems: 'center',
    gap: 4,
  },
  label: {
    fontSize: 12,
    color: COLORS.foreground,
    fontWeight: '500',
  },
});
