import { StyleSheet, ScrollView, useColorScheme } from 'react-native';
import { Text, View } from '@/components/Themed';
import { MaterialIcons } from '@expo/vector-icons';

export default function HistoryScreen() {
  const colorScheme = useColorScheme();

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

  const COLORS = colorScheme === 'dark' ? DARK_COLORS : LIGHT_COLORS;

  const chatHistory = [
    {
      id: 1,
      title: 'Вопрос о погоде',
      preview: 'Какая погода в Москве?',
      date: 'Сегодня',
    },
    {
      id: 2,
      title: 'Помощь с кодом',
      preview: 'Помоги написать функцию на Python',
      date: 'Вчера',
    },
    {
      id: 3,
      title: 'Расчёты',
      preview: 'Посчитай 123 * 456 + 789',
      date: '2 дня назад',
    },
  ];

  return (
    <View style={[styles.container, { backgroundColor: COLORS.background }]}>
      <View style={[styles.header, { borderBottomColor: COLORS.border }]}>
        <Text style={[styles.headerTitle, { color: COLORS.foreground }]}>
          📚 История чатов
        </Text>
      </View>

      <ScrollView style={styles.list}>
        {chatHistory.map((chat) => (
          <View
            key={chat.id}
            style={[
              styles.chatItem,
              { backgroundColor: COLORS.surface, borderColor: COLORS.border },
            ]}
          >
            <View style={styles.chatContent}>
              <Text style={[styles.chatTitle, { color: COLORS.foreground }]}>
                {chat.title}
              </Text>
              <Text style={[styles.chatPreview, { color: COLORS.muted }]}>
                {chat.preview}
              </Text>
              <Text style={[styles.chatDate, { color: COLORS.muted }]}>
                {chat.date}
              </Text>
            </View>
            <MaterialIcons name="chevron-right" size={24} color={COLORS.muted} />
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    borderBottomWidth: 1,
    paddingHorizontal: 16,
    paddingVertical: 16,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  list: {
    flex: 1,
    paddingHorizontal: 12,
    paddingVertical: 12,
  },
  chatItem: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 12,
    borderWidth: 1,
    padding: 16,
    marginVertical: 8,
  },
  chatContent: {
    flex: 1,
  },
  chatTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  chatPreview: {
    fontSize: 14,
    marginBottom: 8,
  },
  chatDate: {
    fontSize: 12,
  },
});
