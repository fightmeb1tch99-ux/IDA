import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router } from "./_core/trpc";
import { z } from "zod";
import { chatWithLLM } from "./chat";

export const appRouter = router({
    // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  chat: router({
    sendMessage: publicProcedure
      .input(z.object({
        message: z.string(),
        conversationHistory: z.array(z.object({
          role: z.enum(['user', 'assistant']),
          content: z.string(),
        })).optional(),
        provider: z.enum(['openai', 'claude', 'gemini', 'mistral', 'groq']).optional(),
        model: z.string().optional(),
        temperature: z.number().min(0).max(2).optional(),
        apiKey: z.string().optional(),
      }))
      .mutation(async ({ input }) => {
        try {
          const messages = [
            ...(input.conversationHistory || []),
            { role: 'user' as const, content: input.message },
          ];

          const response = await chatWithLLM(messages, {
            provider: input.provider,
            model: input.model,
            temperature: input.temperature,
            apiKey: input.apiKey,
          });
          return { success: true, response };
        } catch (error) {
          console.error('Chat error:', error);
          const message = error instanceof Error ? error.message : 'Failed to get response from LLM';
          throw new Error(message);
        }
      }),
  }),

  // TODO: add feature routers here, e.g.
  // todo: router({
  //   list: protectedProcedure.query(({ ctx }) =>
  //     db.getUserTodos(ctx.user.id)
  //   ),
  // }),
});

export type AppRouter = typeof appRouter;
