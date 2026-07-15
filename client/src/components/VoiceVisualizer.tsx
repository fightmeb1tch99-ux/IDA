import { useEffect, useRef, useState } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { drawCanvasGrid } from '@/lib/canvas';

interface FrequencyData {
  frequencies: Uint8Array;
  average: number;
}

export default function VoiceVisualizer() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const audioContextRef = useRef<AudioContext | null>(null as any);
  const analyserRef = useRef<AnalyserNode | null>(null as any);
  const streamRef = useRef<MediaStream | null>(null as any);
  const animationFrameRef = useRef<number | undefined>(undefined);
  const [isListening, setIsListening] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [frequency, setFrequency] = useState(0);
  const [decibels, setDecibels] = useState(-100);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const drawVisualization = () => {
      if (!analyserRef.current) {
        animationFrameRef.current = requestAnimationFrame(drawVisualization);
        return;
      }

      const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
      analyserRef.current.getByteFrequencyData(dataArray);

      // Фон
      ctx.fillStyle = '#0a0e1a';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      drawCanvasGrid(ctx, canvas);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const barCount = dataArray.length / 4;
      const barWidth = (canvas.width / 2) / barCount;

      // Вычисляем среднюю частоту и громкость
      let sum = 0;
      for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
      }
      const average = sum / dataArray.length;
      const db = 20 * Math.log10(Math.max(average / 255, 0.001));

      setFrequency(Math.round(average));
      setDecibels(Math.round(db));

      // Радиальная визуализация
      for (let i = 0; i < barCount; i++) {
        const value = dataArray[i * 4] / 255;
        const angle = (i / barCount) * Math.PI * 2;
        const radius = 50 + value * 150;

        const x1 = centerX + Math.cos(angle) * 50;
        const y1 = centerY + Math.sin(angle) * 50;
        const x2 = centerX + Math.cos(angle) * radius;
        const y2 = centerY + Math.sin(angle) * radius;

        const hue = (i / barCount * 360 + Date.now() / 20) % 360;
        ctx.strokeStyle = `hsla(${hue}, 100%, 50%, ${0.3 + value * 0.7})`;
        ctx.lineWidth = 2 + value * 4;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
      }

      // Центральный круг
      const pulseSize = 30 + average * 0.3;
      const hue = (Date.now() / 20) % 360;

      ctx.fillStyle = `hsla(${hue}, 100%, 50%, 0.2)`;
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize * 2, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = `hsla(${hue}, 100%, 50%, 0.4)`;
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(centerX, centerY, pulseSize * 0.5, 0, Math.PI * 2);
      ctx.fill();

      // Волновая форма
      const waveData = new Uint8Array(analyserRef.current.fftSize);
      analyserRef.current.getByteTimeDomainData(waveData);

      ctx.strokeStyle = `hsla(${hue}, 100%, 50%, 0.6)`;
      ctx.lineWidth = 2;
      ctx.beginPath();

      const sliceWidth = canvas.width / waveData.length;
      let x = 0;

      for (let i = 0; i < waveData.length; i++) {
        const v = waveData[i] / 128.0;
        const y = (v * canvas.height) / 2;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }

        x += sliceWidth;
      }

      ctx.lineTo(canvas.width, canvas.height / 2);
      ctx.stroke();

      animationFrameRef.current = requestAnimationFrame(drawVisualization);
    };

    if (isListening) {
      drawVisualization();
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isListening]);

  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      audioContextRef.current = audioContext;

      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 2048;
      analyserRef.current = analyser;

      const source = audioContext.createMediaStreamSource(stream);
      source.connect(analyser);

      setIsListening(true);
    } catch (error) {
      console.error('Ошибка доступа к микрофону:', error);
      alert('Не удалось получить доступ к микрофону');
    }
  };

  const stopListening = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }

    setIsListening(false);
    setFrequency(0);
    setDecibels(-100);
  };

  const toggleMute = () => {
    if (streamRef.current) {
      streamRef.current.getAudioTracks().forEach(track => {
        track.enabled = !track.enabled;
      });
      setIsMuted(!isMuted);
    }
  };

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-3xl font-bold text-cyan-400 mb-2">🎤 Голосовая визуализация</h1>
        <p className="text-gray-400">
          Говорите в микрофон и смотрите как анимация реагирует на ваш голос в реальном времени
        </p>
      </div>

      <div className="bg-black border border-cyan-500/30 rounded-lg overflow-hidden">
        <canvas
          ref={canvasRef}
          width={800}
          height={600}
          className="w-full bg-gradient-to-br from-slate-950 to-black"
        />
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-slate-900/50 border border-blue-500/30 p-4 rounded-lg">
          <div className="text-sm text-gray-400 mb-1">Частота</div>
          <div className="text-2xl font-bold text-blue-400">{frequency}</div>
        </div>
        <div className="bg-slate-900/50 border border-cyan-500/30 p-4 rounded-lg">
          <div className="text-sm text-gray-400 mb-1">Громкость</div>
          <div className="text-2xl font-bold text-cyan-400">{decibels} dB</div>
        </div>
        <div className="bg-slate-900/50 border border-green-500/30 p-4 rounded-lg">
          <div className="text-sm text-gray-400 mb-1">Статус</div>
          <div className="text-2xl font-bold text-green-400">
            {isListening ? '🎙️ Слушаю' : '⏸️ Ожидание'}
          </div>
        </div>
      </div>

      <div className="flex gap-3">
        {!isListening ? (
          <Button
            onClick={startListening}
            className="flex-1 bg-cyan-600 hover:bg-cyan-700 text-white flex items-center justify-center gap-2"
          >
            <Mic size={20} />
            Начать слушать
          </Button>
        ) : (
          <>
            <Button
              onClick={stopListening}
              className="flex-1 bg-red-600 hover:bg-red-700 text-white flex items-center justify-center gap-2"
            >
              <MicOff size={20} />
              Остановить
            </Button>
            <Button
              onClick={toggleMute}
              className={`flex-1 ${isMuted ? 'bg-orange-600 hover:bg-orange-700' : 'bg-green-600 hover:bg-green-700'} text-white`}
            >
              {isMuted ? '🔇 Без звука' : '🔊 Со звуком'}
            </Button>
          </>
        )}
      </div>

      <div className="bg-slate-900/50 border border-purple-500/30 p-4 rounded-lg">
        <h3 className="text-lg font-semibold text-purple-400 mb-3">📊 Как это работает?</h3>
        <ul className="space-y-2 text-sm text-gray-300">
          <li>🎙️ <span className="text-cyan-400">Микрофон</span> — захватывает ваш голос в реальном времени</li>
          <li>📈 <span className="text-blue-400">Спектр анализатор</span> — показывает частотный спектр звука</li>
          <li>🌈 <span className="text-green-400">Радиальная визуализация</span> — полосы реагируют на громкость</li>
          <li>💫 <span className="text-yellow-400">Пульсирующий центр</span> — пульсирует в ритме звука</li>
          <li>〰️ <span className="text-purple-400">Волновая форма</span> — показывает форму звуковой волны</li>
        </ul>
      </div>
    </div>
  );
}
