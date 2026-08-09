import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Card } from '@/components/ui/card';
import DashboardLayout from '@/components/DashboardLayout';

interface Neuron {
  id: number;
  x: number;
  y: number;
  layer: number;
  activity: number;
  connections: number[];
}

interface Connection {
  from: number;
  to: number;
  strength: number;
  animated: boolean;
}

export default function NeuralNetwork() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [neurons, setNeurons] = useState<Neuron[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [isAnimating, setIsAnimating] = useState(true);
  const [growthRate, setGrowthRate] = useState(0.5);
  const [complexity, setComplexity] = useState(3);
  const [generation, setGeneration] = useState(0);
  const animationFrameRef = useRef<number | undefined>(undefined);
  const timeRef = useRef(0);

  useEffect(() => {
    const initializeNetwork = () => {
      const newNeurons: Neuron[] = [];
      const newConnections: Connection[] = [];

      const layers = complexity;
      const neuronsPerLayer = 8;
      let neuronId = 0;

      for (let layer = 0; layer < layers; layer++) {
        for (let i = 0; i < neuronsPerLayer; i++) {
          const angle = (i / neuronsPerLayer) * Math.PI * 2;
          const radius = 100 + layer * 80;
          const x = 400 + Math.cos(angle) * radius;
          const y = 300 + Math.sin(angle) * radius;

          newNeurons.push({
            id: neuronId,
            x,
            y,
            layer,
            activity: Math.random() * 0.5,
            connections: [] as number[],
          });
          neuronId++;
        }
      }

      for (let i = 0; i < newNeurons.length; i++) {
        const neuron = newNeurons[i];
        const connectionsCount = Math.floor(Math.random() * 4) + 2;

        for (let j = 0; j < connectionsCount; j++) {
          const targetLayer = neuron.layer + 1;
          if (targetLayer < layers) {
            const targetNeurons = newNeurons.filter(n => n.layer === targetLayer);
            if (targetNeurons.length > 0) {
              const target = targetNeurons[Math.floor(Math.random() * targetNeurons.length)];
              neuron.connections.push(target.id);

              newConnections.push({
                from: neuron.id,
                to: target.id,
                strength: Math.random() * 0.7 + 0.3,
                animated: Math.random() > 0.5 as boolean,
              });
            }
          }
        }
      }

      setNeurons(newNeurons);
      setConnections(newConnections);
    };

    initializeNetwork();
  }, [complexity]);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      timeRef.current += 0.016;

      ctx.fillStyle = '#0a0e1a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.strokeStyle = 'rgba(6, 182, 212, 0.05)';
      ctx.lineWidth = 1;
      for (let i = 0; i < canvas.width; i += 40) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
      }
      for (let i = 0; i < canvas.height; i += 40) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
      }

      const updatedNeurons = neurons.map(neuron => ({
        ...neuron,
        activity: Math.sin(timeRef.current * (0.5 + neuron.layer * 0.1) + neuron.id) * 0.5 + 0.5,
      }));

      connections.forEach(connection => {
        const fromNeuron = updatedNeurons.find(n => n.id === connection.from);
        const toNeuron = updatedNeurons.find(n => n.id === connection.to);

        if (fromNeuron && toNeuron) {
          const activity = (fromNeuron.activity + toNeuron.activity) / 2;
          const strength = connection.strength * (0.5 + activity * 0.5);

          const hue = 180 + activity * 60;
          ctx.strokeStyle = `hsla(${hue}, 100%, 50%, ${strength * 0.6})`;
          ctx.lineWidth = 1 + strength * 2;
          ctx.lineCap = 'round';

          ctx.beginPath();
          ctx.moveTo(fromNeuron.x, fromNeuron.y);
          ctx.lineTo(toNeuron.x, toNeuron.y);
          ctx.stroke();
        }
      });

      updatedNeurons.forEach(neuron => {
        const radius = 4 + neuron.activity * 6;
        const hue = 180 + neuron.activity * 60;

        ctx.fillStyle = `hsla(${hue}, 100%, 50%, ${neuron.activity * 0.3})`;
        ctx.beginPath();
        ctx.arc(neuron.x, neuron.y, radius * 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = `hsl(${hue}, 100%, 50%)`;
        ctx.beginPath();
        ctx.arc(neuron.x, neuron.y, radius, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(neuron.x, neuron.y, radius * 0.4, 0, Math.PI * 2);
        ctx.fill();
      });

      setNeurons(updatedNeurons);

      if (isAnimating) {
        animationFrameRef.current = requestAnimationFrame(animate);
      }
    };

    if (isAnimating) {
      animationFrameRef.current = requestAnimationFrame(animate);
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isAnimating, neurons, connections]);

  const handleGrow = () => {
    setGeneration(prev => prev + 1);
    setComplexity(prev => Math.min(prev + 1, 6));
  };

  const handleReset = () => {
    setGeneration(0);
    setComplexity(3);
    timeRef.current = 0;
  };

  return (
    <div className="space-y-6 p-6">
        <div>
          <h1 className="text-3xl font-bold text-cyan-400 mb-2">🧠 Нейронные связи IDA</h1>
          <p className="text-gray-400">
            Визуализация развития нейросети. Каждый узел — нейрон, линии — синаптические связи.
            Цвет показывает активность: голубой = низкая, зелёный = высокая.
          </p>
        </div>

        <Card className="bg-black border-cyan-500/30 overflow-hidden">
          <canvas
            ref={canvasRef}
            width={800}
            height={600}
            className="w-full bg-gradient-to-br from-slate-950 to-black"
          />
        </Card>

        <div className="grid grid-cols-4 gap-4">
          <Card className="bg-slate-900/50 border-blue-500/30 p-4">
            <div className="text-sm text-gray-400 mb-1">Поколение</div>
            <div className="text-2xl font-bold text-blue-400">{generation}</div>
          </Card>
          <Card className="bg-slate-900/50 border-cyan-500/30 p-4">
            <div className="text-sm text-gray-400 mb-1">Слои нейронов</div>
            <div className="text-2xl font-bold text-cyan-400">{complexity}</div>
          </Card>
          <Card className="bg-slate-900/50 border-green-500/30 p-4">
            <div className="text-sm text-gray-400 mb-1">Всего нейронов</div>
            <div className="text-2xl font-bold text-green-400">{neurons.length}</div>
          </Card>
          <Card className="bg-slate-900/50 border-purple-500/30 p-4">
            <div className="text-sm text-gray-400 mb-1">Синапсов</div>
            <div className="text-2xl font-bold text-purple-400">{connections.length}</div>
          </Card>
        </div>

        <Card className="bg-slate-900/50 border-blue-500/30 p-6 space-y-4">
          <div>
            <label className="text-sm text-gray-400 mb-2 block">
              Скорость роста: {(growthRate * 100).toFixed(0)}%
            </label>
            <Slider
              value={[growthRate]}
              onValueChange={(value) => setGrowthRate(value[0])}
              min={0}
              max={1}
              step={0.1}
              className="w-full"
            />
          </div>

          <div className="flex gap-3">
            <Button
              onClick={() => setIsAnimating(!isAnimating)}
              className="flex-1 bg-cyan-600 hover:bg-cyan-700 text-white"
            >
              {isAnimating ? '⏸ Пауза' : '▶ Воспроизведение'}
            </Button>
            <Button
              onClick={handleGrow}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white"
            >
              🌱 Развить сеть
            </Button>
            <Button
              onClick={handleReset}
              className="flex-1 bg-red-600 hover:bg-red-700 text-white"
            >
              🔄 Сброс
            </Button>
          </div>
        </Card>

        <Card className="bg-slate-900/50 border-purple-500/30 p-4">
          <h3 className="text-lg font-semibold text-purple-400 mb-3">📊 Как это работает?</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>🔵 <span className="text-cyan-400">Нейроны</span> — узлы обработки информации</li>
            <li>🔗 <span className="text-blue-400">Синапсы</span> — связи между нейронами</li>
            <li>💫 <span className="text-green-400">Активность</span> — пульсирующие волны сигналов</li>
            <li>📈 <span className="text-yellow-400">Развитие</span> — добавление новых слоёв и связей</li>
            <li>🧠 <span className="text-purple-400">Обучение</span> — укрепление важных синапсов</li>
          </ul>
        </Card>
    </div>
  );
}
