import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Trash2, MessageSquare } from 'lucide-react';

const chatHistory = [
  {
    id: 1,
    title: 'Вопрос о погоде',
    preview: 'Какая погода в Москве?',
    date: 'Сегодня, 14:30',
    messages: 5,
  },
  {
    id: 2,
    title: 'Помощь с кодом',
    preview: 'Помоги написать функцию на Python',
    date: 'Вчера, 10:15',
    messages: 12,
  },
  {
    id: 3,
    title: 'Расчёты',
    preview: 'Посчитай 123 * 456 + 789',
    date: '2 дня назад, 16:45',
    messages: 3,
  },
  {
    id: 4,
    title: 'Информация о проекте',
    preview: 'Расскажи про IDA OS v3.0',
    date: '3 дня назад, 09:20',
    messages: 8,
  },
];

export default function History() {
  return (
    <div className="space-y-4 animate-fadeIn">
      <h2 className="text-2xl font-bold text-glow mb-6">История чатов</h2>
      {chatHistory.map((chat) => (
        <Card key={chat.id} className="card-cyber p-4 hover:scale-105 transition-transform">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="font-semibold text-foreground mb-1">{chat.title}</h3>
              <p className="text-sm text-muted-foreground mb-2 line-clamp-2">{chat.preview}</p>
              <div className="flex items-center gap-4 text-xs text-muted-foreground">
                <span>{chat.date}</span>
                <span className="flex items-center gap-1">
                  <MessageSquare className="w-3 h-3" />
                  {chat.messages} сообщений
                </span>
              </div>
            </div>
            <div className="flex gap-2 ml-4">
              <Button variant="ghost" size="sm" className="hover:text-primary">
                Открыть
              </Button>
              <Button variant="ghost" size="sm" className="hover:text-destructive">
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}

