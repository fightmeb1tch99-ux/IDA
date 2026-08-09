import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { useLocation } from 'wouter';
import { trpc } from '@/lib/trpc';

export default function Login() {
  const [, setLocation] = useLocation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState('');

  const handleDemoMode = () => {
    localStorage.setItem('demoMode', 'true');
    localStorage.setItem('demoUser', JSON.stringify({
      id: 999,
      name: 'Demo User',
      email: 'demo@example.com',
      role: 'user'
    }));
    setLocation('/dashboard');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isRegister) {
        // Регистрация
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name }),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || 'Ошибка регистрации');
        }

        setEmail('');
        setPassword('');
        setName('');
        setIsRegister(false);
        setError('Аккаунт создан! Теперь войдите.');
      } else {
        // Вход
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || 'Ошибка входа');
        }

        setLocation('/dashboard');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-black p-4">
      <Card className="w-full max-w-md bg-slate-900/50 border-cyan-500/30 p-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-cyan-400 mb-2">AI IDA</h1>
          <p className="text-gray-400">
            {isRegister ? 'Создать аккаунт' : 'Вход в систему'}
          </p>
        </div>

        {/* Demo Button */}
        <div className="mb-6 pb-6 border-b border-blue-500/30">
          <Button
            onClick={handleDemoMode}
            className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold"
          >
            🎮 Попробовать Demo
          </Button>
          <p className="text-gray-500 text-xs mt-2 text-center">Временный доступ без регистрации (30 мин)</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegister && (
            <div>
              <label className="text-sm text-gray-400 mb-1 block">Имя</label>
              <Input
                type="text"
                placeholder="Ваше имя"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="bg-slate-800 border-blue-500/30 text-white"
                required
              />
            </div>
          )}

          <div>
            <label className="text-sm text-gray-400 mb-1 block">Email</label>
            <Input
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="bg-slate-800 border-blue-500/30 text-white"
              required
            />
          </div>

          <div>
            <label className="text-sm text-gray-400 mb-1 block">Пароль</label>
            <Input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="bg-slate-800 border-blue-500/30 text-white"
              required
            />
          </div>

          {error && (
            <div className={`p-3 rounded text-sm ${error.includes('создан') ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'}`}>
              {error}
            </div>
          )}

          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-cyan-600 hover:bg-cyan-700 text-white"
          >
            {isLoading ? 'Загрузка...' : isRegister ? 'Создать аккаунт' : 'Войти'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            {isRegister ? 'Уже есть аккаунт?' : 'Нет аккаунта?'}
            <button
              onClick={() => {
                setIsRegister(!isRegister);
                setError('');
              }}
              className="text-cyan-400 hover:text-cyan-300 ml-1 underline"
            >
              {isRegister ? 'Войти' : 'Зарегистрироваться'}
            </button>
          </p>
        </div>
      </Card>
    </div>
  );
}
