import OpenAI from "openai";

export type LLMProvider = "openai" | "claude" | "gemini" | "mistral" | "groq";

export interface LLMConfig {
  provider: LLMProvider;
  model: string;
  apiKey: string;
  temperature?: number;
  maxTokens?: number;
}

export interface LLMResponse {
  content: string;
  provider: LLMProvider;
  model: string;
  tokensUsed?: number;
}

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

type OpenAICompatibleResponse = {
  choices?: Array<{
    message?: {
      content?: string;
    };
  }>;
  usage?: {
    total_tokens?: number;
  };
};

export class LLMManager {
  private config: LLMConfig;

  constructor(config: LLMConfig) {
    this.config = config;
  }

  async chat(messages: ChatMessage[]): Promise<LLMResponse> {
    switch (this.config.provider) {
      case "openai":
        return this.chatOpenAI(messages);
      case "claude":
        return this.chatClaude(messages);
      case "gemini":
        return this.chatGemini(messages);
      case "groq":
        return this.chatGroq(messages);
      case "mistral":
        return this.chatMistral(messages);
      default:
        throw new Error(`Unknown provider: ${this.config.provider}`);
    }
  }

  private async chatOpenAI(messages: ChatMessage[]): Promise<LLMResponse> {
    const openai = new OpenAI({ apiKey: this.config.apiKey });
    const response = await openai.chat.completions.create({
      model: this.config.model,
      messages,
      temperature: this.config.temperature ?? 0.7,
      max_tokens: this.config.maxTokens ?? 1000,
    });
    return {
      content: response.choices[0]?.message.content || "",
      provider: "openai",
      model: this.config.model,
      tokensUsed: response.usage?.total_tokens,
    };
  }

  private async chatClaude(messages: ChatMessage[]): Promise<LLMResponse> {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.config.apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: this.config.model,
        max_tokens: this.config.maxTokens ?? 1000,
        messages,
      }),
    });
    const data = await response.json() as any;
    return {
      content: data.content?.[0]?.text || "",
      provider: "claude",
      model: this.config.model,
      tokensUsed: data.usage?.input_tokens,
    };
  }

  private async chatGemini(messages: ChatMessage[]): Promise<LLMResponse> {
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${this.config.model}:generateContent?key=${this.config.apiKey}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: messages.map((m) => ({
          role: m.role === "user" ? "user" : "model",
          parts: [{ text: m.content }],
        })),
      }),
    });
    const data = await response.json() as any;
    return {
      content: data.candidates?.[0]?.content?.parts?.[0]?.text || "",
      provider: "gemini",
      model: this.config.model,
    };
  }

  private async chatOpenAICompatible(
    provider: "groq" | "mistral",
    endpoint: string,
    messages: ChatMessage[],
    includeUsage: boolean
  ): Promise<LLMResponse> {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({
        model: this.config.model,
        messages,
        temperature: this.config.temperature ?? 0.7,
        max_tokens: this.config.maxTokens ?? 1000,
      }),
    });
    const data = await response.json() as OpenAICompatibleResponse;
    const result: LLMResponse = {
      content: data.choices?.[0]?.message?.content || "",
      provider,
      model: this.config.model,
    };

    if (includeUsage) {
      result.tokensUsed = data.usage?.total_tokens;
    }

    return result;
  }

  private async chatGroq(messages: ChatMessage[]): Promise<LLMResponse> {
    return this.chatOpenAICompatible(
      "groq",
      "https://api.groq.com/openai/v1/chat/completions",
      messages,
      true
    );
  }

  private async chatMistral(messages: ChatMessage[]): Promise<LLMResponse> {
    return this.chatOpenAICompatible(
      "mistral",
      "https://api.mistral.ai/v1/chat/completions",
      messages,
      false
    );
  }

  updateConfig(config: Partial<LLMConfig>) {
    this.config = { ...this.config, ...config };
  }

  getAvailableModels(): Record<LLMProvider, string[]> {
    return {
      openai: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
      claude: ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"],
      gemini: ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
      groq: ["mixtral-8x7b-32768", "llama-3-70b-8192", "llama-3-8b-8192"],
      mistral: ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"],
    };
  }
}

export default LLMManager;
