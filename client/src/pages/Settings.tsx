import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import DashboardLayout from "@/components/DashboardLayout";
import { toast } from "sonner";

type LLMProvider = "openai" | "claude" | "gemini" | "mistral" | "groq";
type Language = "russian" | "yakut" | "english";

const PROVIDERS = {
  openai: { name: "OpenAI", models: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"], color: "from-green-500 to-emerald-600" },
  claude: { name: "Claude (Anthropic)", models: ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"], color: "from-orange-500 to-red-600" },
  gemini: { name: "Gemini (Google)", models: ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"], color: "from-blue-500 to-cyan-600" },
  groq: { name: "Groq", models: ["mixtral-8x7b-32768", "llama-3-70b-8192", "llama-3-8b-8192"], color: "from-purple-500 to-pink-600" },
  mistral: { name: "Mistral AI", models: ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"], color: "from-yellow-500 to-orange-600" },
};

export default function Settings() {
  const [provider, setProvider] = useState<LLMProvider>("openai");
  const [model, setModel] = useState("gpt-4o");
  const [temperature, setTemperature] = useState(0.7);
  const [language, setLanguage] = useState<Language>("russian");
  const [apiKey, setApiKey] = useState("");
  const [showApiKey, setShowApiKey] = useState(false);

  const handleSaveSettings = () => {
    localStorage.setItem("llm_provider", provider);
    localStorage.setItem("llm_model", model);
    localStorage.setItem("llm_temperature", temperature.toString());
    localStorage.setItem("llm_api_key", apiKey);
    localStorage.setItem("language", language);
    toast.success("✅ Настройки сохранены!");
  };

  const handleResetSettings = () => {
    setProvider("openai");
    setModel("gpt-4o");
    setTemperature(0.7);
    setLanguage("russian");
    setApiKey("");
    localStorage.clear();
    toast.info("🔄 Настройки сброшены");
  };

  return (
    <DashboardLayout>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Заголовок */}
          <div className="border-l-4 border-cyan-500 pl-6 py-4">
            <h1 className="text-4xl font-bold text-white mb-2">⚙️ Настройки</h1>
            <p className="text-cyan-300">Выбери провайдера ИИ и настрой параметры</p>
          </div>

          {/* Выбор провайдера */}
          <Card className="bg-slate-800/50 border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">🤖 Выбор провайдера ИИ</h2>
            <p className="text-slate-300 mb-4 text-sm">Выбери провайдера, если основной не работает</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {(Object.entries(PROVIDERS) as [LLMProvider, typeof PROVIDERS[LLMProvider]][]).map(([key, prov]) => (
                <button
                  key={key}
                  onClick={() => {
                    setProvider(key);
                    setModel(prov.models[0]);
                  }}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    provider === key
                      ? `border-cyan-500 bg-gradient-to-r ${prov.color} text-white`
                      : "border-slate-600 bg-slate-700/30 text-slate-300 hover:border-slate-500"
                  }`}
                >
                  <div className="font-semibold">{prov.name}</div>
                  <div className="text-xs opacity-75">{prov.models.length} моделей</div>
                </button>
              ))}
            </div>
          </Card>

          {/* Выбор модели */}
          <Card className="bg-slate-800/50 border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">📋 Модель</h2>
            <Select value={model} onValueChange={setModel}>
              <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                {PROVIDERS[provider].models.map((m) => (
                  <SelectItem key={m} value={m} className="text-white hover:bg-slate-700">
                    {m}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </Card>

          {/* Температура */}
          <Card className="bg-slate-800/50 border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">🌡️ Температура</h2>
            <p className="text-slate-300 text-sm mb-4">
              {temperature < 0.3 ? "🧊 Детерминированно" : temperature < 0.7 ? "⚖️ Сбалансировано" : "🔥 Творчески"}
            </p>
            <Slider
              value={[temperature]}
              onValueChange={(val) => setTemperature(val[0])}
              min={0}
              max={1}
              step={0.1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-slate-400 mt-2">
              <span>0 (точно)</span>
              <span className="font-bold text-cyan-400">{temperature.toFixed(1)}</span>
              <span>1 (творчески)</span>
            </div>
          </Card>

          {/* API Ключ */}
          <Card className="bg-slate-800/50 border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">🔑 API Ключ ({provider.toUpperCase()})</h2>
            <p className="text-slate-300 text-sm mb-4">Введи ключ для {PROVIDERS[provider].name}</p>
            <div className="flex gap-2">
              <Input
                type={showApiKey ? "text" : "password"}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-... или другой ключ"
                className="bg-slate-700 border-slate-600 text-white placeholder:text-slate-500"
              />
              <Button
                onClick={() => setShowApiKey(!showApiKey)}
                variant="outline"
                className="border-slate-600 text-slate-300"
              >
                {showApiKey ? "🙈" : "👁️"}
              </Button>
            </div>
          </Card>

          {/* Язык */}
          <Card className="bg-slate-800/50 border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">🌍 Язык интерфейса</h2>
            <Select value={language} onValueChange={(val) => setLanguage(val as Language)}>
              <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="russian" className="text-white hover:bg-slate-700">
                  🇷🇺 Русский
                </SelectItem>
                <SelectItem value="yakut" className="text-white hover:bg-slate-700">
                  🇷🇺 Якутский (Sakha)
                </SelectItem>
                <SelectItem value="english" className="text-white hover:bg-slate-700">
                  🇬🇧 English
                </SelectItem>
              </SelectContent>
            </Select>
          </Card>

          {/* Кнопки действий */}
          <div className="flex gap-4 pt-4">
            <Button
              onClick={handleSaveSettings}
              className="flex-1 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold py-3 rounded-lg"
            >
              ✅ Сохранить настройки
            </Button>
            <Button
              onClick={handleResetSettings}
              variant="outline"
              className="flex-1 border-red-500 text-red-400 hover:bg-red-500/10"
            >
              🔄 Сбросить
            </Button>
          </div>

          {/* Информация */}
          <Card className="bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border-cyan-500/30 p-6">
            <h3 className="text-white font-bold mb-2">ℹ️ Информация</h3>
            <ul className="text-slate-300 text-sm space-y-1">
              <li>✅ Все настройки сохраняются локально</li>
              <li>✅ Ключи никогда не отправляются на сервер</li>
              <li>✅ Можешь менять провайдера в любой момент</li>
              <li>✅ Если один ИИ не работает, используй другой</li>
            </ul>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
