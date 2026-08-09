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
    if (!process.env.OPENAI_API_KEY) {
      throw new Error('OPENAI_API_KEY is not configured');
    }

    // Ensure we have at least one message
    if (!messages || messages.length === 0) {
      throw new Error('No messages provided');
    }

    // Add system message if not present
    const systemMessage: ChatMessage = {
      role: 'system',
      content: 'You are AI IDA, a helpful personal assistant. Respond in the same language as the user.'
    };

    const allMessages = messages[0]?.role === 'system' 
      ? messages 
      : [systemMessage, ...messages];

    const response = await openai.chat.completions.create({
      model,
      messages: allMessages as any,
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
    if (error instanceof Error) {
      throw new Error(`Chat API Error: ${error.message}`);
    }
    throw new Error('Unknown error occurred in chat API');
  }
}

export async function* chatWithGPTStream(
  messages: ChatMessage[],
  model: string = 'gpt-4o-mini'
) {
  try {
    if (!process.env.OPENAI_API_KEY) {
      throw new Error('OPENAI_API_KEY is not configured');
    }

    if (!messages || messages.length === 0) {
      throw new Error('No messages provided');
    }

    const systemMessage: ChatMessage = {
      role: 'system',
      content: 'You are AI IDA, a helpful personal assistant. Respond in the same language as the user.'
    };

    const allMessages = messages[0]?.role === 'system' 
      ? messages 
      : [systemMessage, ...messages];

    const stream = await openai.chat.completions.create({
      model,
      messages: allMessages as any,
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
    if (error instanceof Error) {
      throw new Error(`Streaming Error: ${error.message}`);
    }
    throw new Error('Unknown error occurred in streaming');
  }
}
