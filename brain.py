import re
from logger import log_debug, log_info


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
    
    def decide_tool(self, text):
        """Decide which tool to use based on user input."""
        return self.parser.parse(text)
    
    def generate_response(self, text, tool_result=None):
        """
        Generate response based on user input and tool results.
        
        Args:
            text (str): User input
            tool_result (str): Result from executed tool
            
        Returns:
            str: Response message
        """
        text_lower = text.lower()
        
        # Greeting responses
        if any(word in text_lower for word in ["привет", "привет!", "привет)", "hi", "hello", "hey"]):
            responses = [
                "Йо 👋",
                "Привет! Как дела?",
                "Салют! 🚀",
            ]
            return responses[hash(text) % len(responses)]
        
        # Name-related responses
        if "как меня зовут" in text_lower or "мое имя" in text_lower:
            name = self.memory.get("name", "я не знаю 😅")
            return f"Тебя зовут {name}"
        
        if "меня зовут" in text_lower:
            # Extract name
            name = re.sub(r"меня зовут\s+", "", text_lower).strip()
            if name:
                self.memory["name"] = name
                log_info(f"User name saved: {name}")
                return f"Ок, запомнил: {name} 📝"
            return "Не понял имя, попробуй ещё раз"
        
        # Help response
        if any(word in text_lower for word in ["помощь", "помоги", "что ты умеешь", "команды"]):
            return self._get_help_message()
        
        # If we have a tool result, return it
        if tool_result:
            return tool_result
        
        # Default response
        return "Я пока не понимаю это 🤖. Напиши 'помощь' для списка команд"
    
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
