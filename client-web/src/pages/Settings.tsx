import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useState } from 'react';
import { toast } from 'sonner';

export default function Settings() {
  const [settings, setSettings] = useState({
    model: 'gpt-4o-mini',
    temperature: 0.7,
    language: 'russian',
    apiKey: '',
  });

  const handleSave = () => {
    toast.success('Настройки сохранены');
  };

  return (
    <div className="space-y-6 animate-fadeIn max-w-2xl">
      <h2 className="text-2xl font-bold text-glow mb-6">Настройки</h2>

      <Card className="card-cyber p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Модель LLM</h3>
        <div className="space-y-4">
          <div>
            <Label className="text-muted-foreground mb-2 block">Выбери модель</Label>
            <Select value={settings.model} onValueChange={(value) => setSettings({ ...settings, model: value })}>
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gpt-4o-mini">GPT-4o Mini (быстро)</SelectItem>
                <SelectItem value="gpt-4o">GPT-4o (точнее)</SelectItem>
                <SelectItem value="gpt-4-turbo">GPT-4 Turbo (мощнее)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <Label className="text-muted-foreground mb-2 block">Температура ({settings.temperature})</Label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={settings.temperature}
              onChange={(e) => setSettings({ ...settings, temperature: parseFloat(e.target.value) })}
              className="w-full"
            />
            <p className="text-xs text-muted-foreground mt-1">
              Ниже = детерминированнее, выше = творче
            </p>
          </div>
        </div>
      </Card>

      <Card className="card-cyber p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Язык интерфейса</h3>
        <div>
          <Label className="text-muted-foreground mb-2 block">Выбери язык</Label>
          <Select value={settings.language} onValueChange={(value) => setSettings({ ...settings, language: value })}>
            <SelectTrigger className="w-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="russian">Русский</SelectItem>
              <SelectItem value="yakut">Якутский</SelectItem>
              <SelectItem value="english">English</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </Card>

      <Card className="card-cyber p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">API Ключ</h3>
        <div>
          <Label className="text-muted-foreground mb-2 block">OpenAI API Key</Label>
          <Input
            type="password"
            placeholder="sk-..."
            value={settings.apiKey}
            onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
            className="w-full"
          />
          <p className="text-xs text-muted-foreground mt-2">
            Твой API ключ хранится локально и никогда не отправляется на серверы
          </p>
        </div>
      </Card>

      <Button onClick={handleSave} className="btn-cyber w-full">
        Сохранить настройки
      </Button>
    </div>
  );
}
