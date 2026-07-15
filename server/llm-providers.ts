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

export class LLMManager {
  private config: LLMConfig;

  constructor(config: LLMConfig) {
    this.config = config;
  }

  async chat(messages: Array<{ role: "user" | "assistant"; content: string }>): Promise<LLMResponse> {
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

  private async postJson(url: string, headers: Record<string, string>, body: unknown, label: string): Promise<any> {
    const response = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      const detail = data?.error?.message || data?.message || response.statusText;
      throw new Error(`${label} API error ${response.status}: ${detail}`);
    }
    return data;
  }

  private async chatOpenAI(messages: Array<{ role: "user" | "assistant"; content: string }>): Promise<LLMResponse> {
    const openai = new OpenAI({ apiKey: this.config.apiKey });
    const response = await openai.chat.completions.create({
      model: this.config.model,
      messages,
      temperature: this.config.temperature ?? 0.7,
      max_tokens: this.config.maxTokens ?? 1000,
    });
    return {
      content: response.choices[0]?.message?.content || "",
      provider: "openai",
      model: this.config.model,
      tokensUsed: response.usage?.total_tokens,
    };
  }

  private async chatClaude(messages: Array<{ role: "user" | "assistant"; content: string }>): Promise<LLMResponse> {
    const data = await this.postJson(
      "https://api.anthropic.com/v1/messages",
      {
        "Content-Type": "application/json",
        "x-api-key": this.config.apiKey,
        "anthropic-version": "2023-06-01",
      },
      {
        model: this.config.model,
        max_tokens: this.config.maxTokens ?? 1000,
        temperature: this.config.temperature ?? 0.7,
        messages,
      },
      "Claude"
    );
    const usage = data.usage;
    return {
      content: data.content?.[0]?.text || "",
      provider: "claude",
      model: this.config.model,
      tokensUsed: usage ? (usage.input_tokens ?? 0) + (usage.output_tokens ?? 0) : undefined,
    };
  }

  private async chatGemini(messages: Array<{ role: "user" | "assistant"; content: string }>): Promise<LLMResponse> {
    const data = await this.postJson(
      `https://generativelanguage.googleapis.com/v1beta/models/${this.config.model}:generateContent`,
      {
        "Content-Type": "application/json",
        "x-goog-api-key": this.config.apiKey,
      },
      {
        contents: messages.map((m) => ({
          role: m.role === "user" ? "user" : "model",
          parts: [{ text: m.content }],
        })),
        generationConfig: {
          temperature: this.config.temperature ?? 0.7,
          maxOutputTokens: this.config.maxTokens ?? 1000,
        },
      },
      "Gemini"
    );
    return {
      content: data.candidates?.[0]?.content?.parts?.[0]?.text || "",
      provider: "gemini",
      model: this.config.model,
      tokensUsed: data.usageMetadata?.totalTokenCount,
    };
  }

  private async chatGroq(messages: Array<{ role: "user" | "assistant"; content: string }>): Promise<LLMResponse> {
    const data = await this.postJson(
      "https://api.groq.com/openai/v1/chat/completions",
      {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.config.apiKey}`,
      },
      {
        model: this.config.model,
        messages,
        temperature: this.config.temperature ?? 0.7,
        max_tokens: this.config.maxTokens ?? 1000,
      },
      "Groq"
    );
    return {
      content: data.choices?.[0]?.message?.content || "",
      provider: "groq",
      model: this.config.model,
      tokensUsed: data.usage?.total_tokens,
    };
  }

  private async chatMistral(messages: Array<{ role: "user" | "assistant"; content: string }>): Promise<LLMResponse> {
    const data = await this.postJson(
      "https://api.mistral.ai/v1/chat/completions",
      {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.config.apiKey}`,
      },
      {
        model: this.config.model,
        messages,
        temperature: this.config.temperature ?? 0.7,
        max_tokens: this.config.maxTokens ?? 1000,
      },
      "Mistral"
    );
    return {
      content: data.choices?.[0]?.message?.content || "",
      provider: "mistral",
      model: this.config.model,
      tokensUsed: data.usage?.total_tokens,
    };
  }

  updateConfig(config: Partial<LLMConfig>) {
    this.config = { ...this.config, ...config };
  }

  getAvailableModels(): Record<LLMProvider, string[]> {
    return {
      openai: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
      claude: ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"],
      gemini: ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
      groq: ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama-3-70b-8192"],
      mistral: ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"],
    };
  }
}

export default LLMManager;
