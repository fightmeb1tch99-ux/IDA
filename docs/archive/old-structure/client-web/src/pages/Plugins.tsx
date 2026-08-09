import { Card } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { useState } from 'react';
import { Cloud, Globe, Zap, Database } from 'lucide-react';

interface Plugin {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  enabled: boolean;
}

const initialPlugins: Plugin[] = [
  {
    id: 'weather',
    name: 'Weather',
    description: 'Получение информации о погоде в любом городе',
    icon: <Cloud className="w-6 h-6" />,
    enabled: true,
  },
  {
    id: 'browser',
    name: 'Browser',
    description: 'Автоматизация браузера и веб-поиск',
    icon: <Globe className="w-6 h-6" />,
    enabled: true,
  },
  {
    id: 'calculator',
    name: 'Calculator',
    description: 'Выполнение математических расчётов',
    icon: <Zap className="w-6 h-6" />,
    enabled: true,
  },
  {
    id: 'database',
    name: 'Database',
    description: 'Работа с базами данных и хранилищем',
    icon: <Database className="w-6 h-6" />,
    enabled: false,
  },
];

export default function Plugins() {
  const [plugins, setPlugins] = useState(initialPlugins);

  const togglePlugin = (id: string) => {
    setPlugins(plugins.map(p => p.id === id ? { ...p, enabled: !p.enabled } : p));
  };

  return (
    <div className="space-y-4 animate-fadeIn">
      <h2 className="text-2xl font-bold text-glow mb-6">Управление плагинами</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {plugins.map((plugin) => (
          <Card key={plugin.id} className="card-cyber p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="text-secondary">{plugin.icon}</div>
                <div>
                  <h3 className="font-semibold text-foreground">{plugin.name}</h3>
                  <p className="text-sm text-muted-foreground">{plugin.description}</p>
                </div>
              </div>
              <Switch
                checked={plugin.enabled}
                onCheckedChange={() => togglePlugin(plugin.id)}
              />
            </div>
            <div className="text-xs text-muted-foreground">
              Статус: <span className={plugin.enabled ? 'text-green-500' : 'text-muted-foreground'}>
                {plugin.enabled ? 'Включен' : 'Отключен'}
              </span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

