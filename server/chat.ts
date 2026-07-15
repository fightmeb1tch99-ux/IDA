import LLMManager, { LLMProvider, LLMResponse } from "./llm-providers";

type ChatMessage = { role: "user" | "assistant"; content: string };

const PROVIDER_ENV_KEYS: Record<LLMProvider, string> = {
  openai: "OPENAI_API_KEY",
  claude: "ANTHROPIC_API_KEY",
  gemini: "GEMINI_API_KEY",
  groq: "GROQ_API_KEY",
  mistral: "MISTRAL_API_KEY",
};

const DEFAULT_MODELS: Record<LLMProvider, string> = {
  openai: "gpt-4o",
  claude: "claude-3-5-sonnet-20241022",
  gemini: "gemini-2.0-flash",
  groq: "llama-3-70b-8192",
  mistral: "mistral-large-latest",
};

export interface ChatOptions {
  provider?: LLMProvider;
  model?: string;
  apiKey?: string;
  temperature?: number;
}

export async function chatWithLLM(
  messages: ChatMessage[],
  options: ChatOptions = {}
): Promise<LLMResponse> {
  const provider = options.provider ?? "openai";
  const model = options.model || DEFAULT_MODELS[provider];
  const apiKey = options.apiKey || process.env[PROVIDER_ENV_KEYS[provider]] || "";
  const temperature = options.temperature ?? 0.7;

  if (!apiKey) {
    throw new Error(
      `Missing API key for provider "${provider}". Set ${PROVIDER_ENV_KEYS[provider]} or provide a key in Settings.`
    );
  }

  // Anthropic and Gemini reject conversations that don't start with a user turn.
  const conversation = dropLeadingAssistant(messages);

  try {
    const manager = new LLMManager({
      provider,
      model,
      apiKey,
      temperature,
      maxTokens: 1000,
    });

    return await manager.chat(conversation);
  } catch (error) {
    console.error(`[Chat] Error with ${provider}:`, error);
    throw error;
  }
}

function dropLeadingAssistant(messages: ChatMessage[]): ChatMessage[] {
  let start = 0;
  while (start < messages.length && messages[start].role === "assistant") {
    start += 1;
  }
  return messages.slice(start);
}

export async function getAvailableModels() {
  const manager = new LLMManager({
    provider: "openai",
    model: "gpt-4o",
    apiKey: "",
  });
  return manager.getAvailableModels();
}
