import re
import os
from logger import log_debug, log_info, log_error
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class CommandParser:
    """Advanced command parser with regex patterns and variations."""
    
    def __init__(self):
        # Define command patterns with variations
        self.patterns = {
            "time": [
                r"(?:какое|которое|скажи|напиши)?\s*время",
                r"текущее время",
                r"сколько времени",
            ],
            "date": [
                r"(?:какая|которая|скажи|напиши)?\s*дата",
                r"текущая дата",
                r"сегодня",
                r"какое число",
            ],
            "create_file": [
                r"создай\s+файл\s+(.+)",
                r"создать\s+файл\s+(.+)",
                r"новый\s+файл\s+(.+)",
            ],
            "run": [
                r"выполни\s+(.+)",
                r"запусти\s+(.+)",
                r"выполнить\s+(.+)",
                r"команда\s+(.+)",
            ],
            "search": [
                r"найди\s+(.+)",
                r"поиск\s+(.+)",
                r"ищи\s+(.+)",
                r"найти\s+(.+)",
                r"гугли\s+(.+)",
            ],
            "help": [
                r"помощь",
                r"помоги",
                r"что ты умеешь",
                r"команды",
                r"справка",
            ],
        }
    
    def parse(self, text):
        """
        Parse user input and return (tool_name, argument).
        
        Args:
            text (str): User input
            
        Returns:
            tuple: (tool_name, argument) or (None, None)
        """
        text = text.lower().strip()
        log_debug(f"Parsing input: {text}")
        
        for tool_name, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    # Extract argument if pattern has a group
                    arg = match.group(1).strip() if match.groups() else None
                    log_debug(f"Matched tool: {tool_name}, arg: {arg}")
                    return (tool_name, arg)
        
        return (None, None)


class Brain:
    """AI Brain for decision making and responses."""
    
    def __init__(self, memory):
        self.memory = memory
        self.parser = CommandParser()
        self.conversation_history = []
        self.client = None
        
        # Initialize OpenAI client if key is present
        api_key = os.getenv("OPENAI_API_KEY")
        if HAS_OPENAI and api_key:
            try:
                # Use Manus pre-configured OpenAI client
                self.client = OpenAI()
                log_info("LLM Brain initialized successfully")
            except Exception as e:
                log_error("Failed to initialize LLM Brain", e)
    
    def decide_tool(self, text):
        """Decide which tool to use based on user input."""
        return self.parser.parse(text)
    
    def generate_response(self, text, tool_result=None):
        """
        Generate response based on user input and tool results.
        """
        text_lower = text.lower()
        
        # 1. Check for system commands (Help)
        if any(word in text_lower for word in ["помощь", "помоги", "что ты умеешь", "команды"]):
            return self._get_help_message()
            
        # 2. If tool result exists, use it as part of the context or direct response
        if tool_result:
            if self.client:
                return self._get_llm_response(f"Результат выполнения команды: {tool_result}. Ответь пользователю на основе этого.")
            return tool_result

        # 3. Use LLM if available for "smart" conversation
        if self.client:
            return self._get_llm_response(text)
        
        # 4. Fallback to basic responses if no LLM
        if any(word in text_lower for word in ["привет", "привет!", "привет)", "hi", "hello", "hey"]):
            return "Йо 👋 Я IDA v 0.1. Чем могу помочь?"
            
        if "как меня зовут" in text_lower:
            name = self.memory.get("name", "я не знаю 😅")
            return f"Тебя зовут {name}"
            
        if "меня зовут" in text_lower:
            name = re.sub(r"меня зовут\s+", "", text_lower).strip()
            if name:
                self.memory["name"] = name
                return f"Ок, запомнил: {name} 📝"
        
        return "Я пока не понимаю это 🤖. Напиши 'помощь' для списка команд"

    def _get_llm_response(self, user_input):
        """Get response from LLM (OpenAI)."""
        try:
            # Build system prompt
            system_prompt = f"""
            Ты - IDA v 0.1, продвинутый ИИ-агент. 
            Твоя цель - помогать пользователю, поддерживать разговор и быть полезным.
            Ты должен отвечать как настоящий GPT, быть вежливым и умным.
            Имя пользователя: {self.memory.get('name', 'Неизвестно')}.
            Если пользователь просит выполнить команду, которую ты уже выполнил (результат предоставлен), прокомментируй результат.
            """
            
            # Prepare messages with history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add last 5 interactions for context
            for interaction in self.conversation_history[-5:]:
                messages.append({"role": "user", "content": interaction["user"]})
                messages.append({"role": "assistant", "content": interaction["response"]})
            
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model="gpt-5-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            if response and response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            return "Извини, я не смог получить ответ от мозга 🧠"
            
        except Exception as e:
            log_error("LLM Error", e)
            return f"Извини, у меня возникла ошибка при общении: {str(e)}"
    
    def _get_help_message(self):
        """Get help message with available commands."""
        help_text = """
📚 **Доступные команды:**

⏰ **Время и дата:**
  - "Какое время?" → текущее время
  - "Какая дата?" → текущая дата

📁 **Работа с файлами:**
  - "Создай файл [имя]" → создать новый файл

🔍 **Поиск:**
  - "Найди [запрос]" → поиск в интернете

⚙️ **Команды:**
  - "Выполни [команда]" → запустить безопасную команду

👤 **Личное:**
  - "Меня зовут [имя]" → сохранить имя
  - "Как меня зовут?" → узнать своё имя

❓ **Справка:**
  - "Помощь" → показать эту справку
        """
        return help_text.strip()
    
    def add_to_history(self, user_input, response):
        """Add interaction to conversation history."""
        self.conversation_history.append({
            "user": user_input,
            "response": response
        })
        log_debug(f"Added to history: {user_input} -> {response[:50]}...")
    
    def get_history(self):
        """Get conversation history."""
        return self.conversation_history
