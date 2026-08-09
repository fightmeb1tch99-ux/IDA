import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Send, Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import { trpc } from '@/lib/trpc';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  error?: boolean;
  isStreaming?: boolean;
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
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const sendMessageMutation = trpc.chat.sendMessage.useMutation();
  const streamingRef = useRef<AbortController | null>(null);

  const scrollToBottom = () => {
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleStreamingResponse = async (userInput: string, conversationHistory: any[]) => {
    try {
      // First, send the message normally to get streaming
      const result = await sendMessageMutation.mutateAsync({
        message: userInput,
        conversationHistory,
      });

      // If streaming not available, use regular response
      if (result.response) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: result.response,
          sender: 'assistant',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);
        toast.success('✓ Ответ получен');
      }
    } catch (error) {
      console.error('Streaming error:', error);
      
      let errorText = 'Ошибка подключения';
      if (error instanceof Error) {
        if (error.message.includes('OPENAI_API_KEY')) {
          errorText = 'OpenAI API ключ не настроен. Свяжитесь с администратором.';
        } else if (error.message.includes('401')) {
          errorText = 'Неверный OpenAI API ключ.';
        } else if (error.message.includes('429')) {
          errorText = 'Слишком много запросов. Попробуй позже.';
        } else if (error.message.includes('timeout')) {
          errorText = 'Соединение истекло. Проверь интернет.';
        } else {
          errorText = error.message;
        }
      }

      toast.error(`❌ ${errorText}`);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `Ошибка: ${errorText}`,
        sender: 'assistant',
        timestamp: new Date(),
        error: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    if (isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    const userInput = inputText;
    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    // Add streaming message placeholder
    const streamingMessageId = (Date.now() + 1).toString();
    const streamingMessage: Message = {
      id: streamingMessageId,
      text: '',
      sender: 'assistant',
      timestamp: new Date(),
      isStreaming: true,
    };
    setMessages((prev) => [...prev, streamingMessage]);

    try {
      // Build conversation history
      const conversationHistory = messages
        .filter(m => m.id !== streamingMessageId)
        .map(m => ({
          role: m.sender === 'user' ? 'user' as const : 'assistant' as const,
          content: m.text,
        }));

      // Simulate streaming by fetching response and updating character by character
      const result = await sendMessageMutation.mutateAsync({
        message: userInput,
        conversationHistory,
      });

      if (!result.response) {
        throw new Error('Empty response from server');
      }

      // Simulate streaming effect - display text character by character
      const response = result.response;
      let displayedText = '';
      
      for (let i = 0; i < response.length; i++) {
        displayedText += response[i];
        
        // Update message with streaming text
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === streamingMessageId
              ? { ...msg, text: displayedText, isStreaming: i < response.length - 1 }
              : msg
          )
        );

        // Add small delay for streaming effect (10ms per character)
        await new Promise((resolve) => setTimeout(resolve, 10));
      }

      // Mark as finished streaming
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === streamingMessageId
            ? { ...msg, isStreaming: false }
            : msg
        )
      );

      toast.success('✓ Ответ получен');
    } catch (error) {
      console.error('Chat error:', error);
      
      let errorText = 'Ошибка подключения';
      if (error instanceof Error) {
        if (error.message.includes('OPENAI_API_KEY')) {
          errorText = 'OpenAI API ключ не настроен. Свяжитесь с администратором.';
        } else if (error.message.includes('401')) {
          errorText = 'Неверный OpenAI API ключ.';
        } else if (error.message.includes('429')) {
          errorText = 'Слишком много запросов. Попробуй позже.';
        } else if (error.message.includes('timeout')) {
          errorText = 'Соединение истекло. Проверь интернет.';
        } else {
          errorText = error.message;
        }
      }

      toast.error(`❌ ${errorText}`);
      
      // Replace streaming message with error
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === streamingMessageId
            ? {
                id: msg.id,
                text: `Ошибка: ${errorText}`,
                sender: 'assistant',
                timestamp: new Date(),
                error: true,
                isStreaming: false,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-screen bg-background animate-fadeIn">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-2 sm:p-4 space-y-3 sm:space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-slideIn`}
          >
            <Card className={`max-w-xs sm:max-w-md card-cyber p-3 sm:p-4 ${
              message.sender === 'user'
                ? 'bg-primary text-primary-foreground'
                : message.error
                ? 'bg-red-900/20 border-red-500/50'
                : 'bg-card'
            }`}>
              <div className="flex items-start gap-2">
                {message.error && <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-red-500" />}
                <div className="flex-1">
                  <p className="text-sm break-words whitespace-pre-wrap">{message.text}</p>
                  {message.isStreaming && <span className="inline-block w-2 h-4 bg-current ml-1 animate-pulse" />}
                  <p className={`text-xs mt-2 ${
                    message.sender === 'user' ? 'opacity-70' : 'text-muted-foreground'
                  }`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>
              </div>
            </Card>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-border p-2 sm:p-4 bg-card">
        <div className="flex gap-2">
          <Input
            placeholder="Напиши сообщение..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            disabled={isLoading}
            className="flex-1 text-sm"
            maxLength={1000}
          />
          <Button
            onClick={handleSendMessage}
            disabled={isLoading || !inputText.trim()}
            className="btn-cyber flex-shrink-0"
            size="sm"
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </Button>
        </div>
        <p className="text-xs text-muted-foreground mt-2 text-right">
          {inputText.length}/1000
        </p>
      </div>
    </div>
  );
}
