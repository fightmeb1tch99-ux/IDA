import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Send, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { trpc } from '@/lib/trpc';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'Привет! Я AI IDA — твой персональный ассистент. Чем я могу помочь?',
      sender: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollViewRef = useRef<HTMLDivElement>(null);
  const sendMessageMutation = trpc.chat.sendMessage.useMutation();

  useEffect(() => {
    scrollViewRef.current?.scrollIntoView({ behavior: 'smooth' });
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
      const conversationHistory = messages
        .filter(m => m.sender !== 'assistant' || m.text !== 'Привет! Я AI IDA — твой персональный ассистент. Чем я могу помочь?')
        .map(m => ({
          role: m.sender === 'user' ? 'user' as const : 'assistant' as const,
          content: m.text,
        }));

      const result = await sendMessageMutation.mutateAsync({
        message: inputText,
        conversationHistory,
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: result.response || 'Извини, я не смог обработать твой запрос.',
        sender: 'assistant',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Ошибка подключения к GPT API');
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Ошибка подключения к GPT. Проверь API ключ и интернет соединение.',
        sender: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-screen bg-background animate-fadeIn">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <Card className={`max-w-xs lg:max-w-md card-cyber p-4 ${
              message.sender === 'user'
                ? 'bg-primary text-primary-foreground'
                : 'bg-card'
            }`}>
              <p className="text-sm">{message.text}</p>
              <p className={`text-xs mt-2 ${
                message.sender === 'user' ? 'opacity-70' : 'text-muted-foreground'
              }`}>
                {formatTime(message.timestamp)}
              </p>
            </Card>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <Card className="card-cyber p-4">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-primary" />
                <span className="text-sm text-muted-foreground">IDA думает...</span>
              </div>
            </Card>
          </div>
        )}
        <div ref={scrollViewRef} />
      </div>

      <div className="border-t border-border p-4 bg-card">
        <div className="flex gap-2">
          <Input
            placeholder="Напиши сообщение..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
            disabled={isLoading}
            className="flex-1"
          />
          <Button
            onClick={handleSendMessage}
            disabled={isLoading || !inputText.trim()}
            className="btn-cyber"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </Button>
        </div>
      </div>
    </div>
  );
}
