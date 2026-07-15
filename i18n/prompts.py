"""
Localized prompt/response strings for IDA OS.

Add a new language by adding a top-level entry with the same set of keys.
:func:`i18n.get_prompt` reads from this table.
"""

DEFAULT_LANGUAGE = "ru"

# Multilingual support: Russian, Sakha (Yakut), English
LANGUAGE_PROMPTS = {
    'ru': {
        'system': "Ты — IDA OS, автономный ИИ-агент. Твоя задача — помогать пользователю. Отвечай на русском языке.",
        'thought': "Ты — IDA OS. Проанализируй задачу шаг за шагом и напиши краткий план действий.\nЗадача: {input}",
        'tool_decision': "System: Identify if any tool is needed for this task: '{input}'. Available tools: weather, calculator, search, stats. Respond ONLY in JSON format: {{\"tool\": \"tool_name\" or null, \"arg\": \"argument\" or null}}",
        'api_error': "OpenAI API key missing.",
        'llm_error': "Ошибка при генерации ответа: {error}",
        'empty_response': "Я выполнил задачу, но не смог сформулировать текстовый ответ. Система работает в штатном режиме.",
        'news_fallback': "Я нашел новости, но не смог их кратко пересказать. Пожалуйста, проверь результаты поиска напрямую.",
    },
    'sah': {
        'system': "Эн — IDA OS, автономнай ИИ-агент. Эн сабай — аат туох кыттыы. Саха тылынан хоруй.",
        'thought': "Эн — IDA OS. Ыйыы сокуоннарын анализ кыл эбэтэр сокуон плана бичи.\nЫйыы: {input}",
        'tool_decision': "System: Identify if any tool is needed for this task: '{input}'. Available tools: weather, calculator, search, stats. Respond ONLY in JSON format: {{\"tool\": \"tool_name\" or null, \"arg\": \"argument\" or null}}",
        'api_error': "OpenAI API ачкы сокуобалаа.",
        'llm_error': "Хоруу уонна сыаналлаах алгыс: {error}",
        'empty_response': "Мин ыйыыны ылыппын, онно эмэ тиэкиэл хоруу сыаналлаах алгыс сыаналлаа алдьатпын.",
        'news_fallback': "Мин сэргэ сыаналлаа сыаналлаа алдьатпын, онно эмэ сокуоннарын кыскаанан сыаналлаа алдьатпын.",
    },
    'en': {
        'system': "You are IDA OS, an autonomous AI agent. Your task is to help the user. Respond in English.",
        'thought': "You are IDA OS. Analyze the task step by step and write a brief action plan.\nTask: {input}",
        'tool_decision': "System: Identify if any tool is needed for this task: '{input}'. Available tools: weather, calculator, search, stats. Respond ONLY in JSON format: {{\"tool\": \"tool_name\" or null, \"arg\": \"argument\" or null}}",
        'api_error': "OpenAI API key missing.",
        'llm_error': "Error generating response: {error}",
        'empty_response': "I completed the task, but couldn't formulate a text response. The system is operating normally.",
        'news_fallback': "I found news, but couldn't summarize them briefly. Please check the search results directly.",
    }
}
