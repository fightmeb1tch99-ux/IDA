import { OpenAI } from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export async function chatWithGPT(
  messages: ChatMessage[],
  model: string = 'gpt-4o-mini'
): Promise<string> {
  try {
    const response = await openai.chat.completions.create({
      model,
      messages: messages as any,
      temperature: 0.7,
      max_tokens: 2000,
    });

    const content = response.choices[0]?.message?.content;
    if (!content) {
      throw new Error('No response from OpenAI');
    }

    return content;
  } catch (error) {
    console.error('OpenAI API error:', error);
    throw error;
  }
}

export async function* chatWithGPTStream(
  messages: ChatMessage[],
  model: string = 'gpt-4o-mini'
) {
  try {
    const stream = await openai.chat.completions.create({
      model,
      messages: messages as any,
      temperature: 0.7,
      max_tokens: 2000,
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        yield content;
      }
    }
  } catch (error) {
    console.error('OpenAI streaming error:', error);
    throw error;
  }
}
