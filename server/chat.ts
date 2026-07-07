import LLMManager, { LLMProvider } from "./llm-providers";

export async function chatWithLLM(
  messages: Array<{ role: "user" | "assistant"; content: string }>,
  provider: LLMProvider = "openai",
  model: string = "gpt-4o",
  apiKey: string = process.env.OPENAI_API_KEY || "",
  temperature: number = 0.7
) {
  try {
    const manager = new LLMManager({
      provider,
      model,
      apiKey,
      temperature,
      maxTokens: 1000,
    });

    const response = await manager.chat(messages);
    return response;
  } catch (error) {
    console.error(`[Chat] Error with ${provider}:`, error);
    throw error;
  }
}

export async function getAvailableModels() {
  const manager = new LLMManager({
    provider: "openai",
    model: "gpt-4o",
    apiKey: "",
  });
  return manager.getAvailableModels();
}
