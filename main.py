"""
AI Agent - Advanced version with security, logging, and improved NLP.

Features:
- Secure command execution with whitelisting
- Comprehensive logging
- Advanced NLP with regex patterns
- Memory management with backups
- Conversation history
"""

import sys
from tools.tools import TOOLS, get_available_tools
from brain import Brain
from memory_manager import MemoryManager
from logger import log_info, log_error, log_warning, log_debug


class AIAgent:
    """Main AI Agent class."""
    
    def __init__(self):
        """Initialize the AI Agent."""
        log_info("Initializing AI Agent...")
        self.memory_manager = MemoryManager()
        self.brain = Brain(self.memory_manager.memory)
        log_info("AI Agent initialized successfully")
    
    def process_input(self, user_input):
        """
        Process user input and generate response.
        
        Args:
            user_input (str): User's input text
            
        Returns:
            str: Agent's response
        """
        if not user_input or not isinstance(user_input, str):
            return "Ошибка: некорректный ввод"
        
        user_input = user_input.strip()
        if not user_input:
            return "Пожалуйста, напиши что-нибудь"
        
        log_debug(f"Processing input: {user_input}")
        
        # Decide which tool to use
        tool_name, arg = self.brain.decide_tool(user_input)
        tool_result = None
        
        # Execute tool if found
        if tool_name and tool_name in TOOLS:
            try:
                tool = TOOLS[tool_name]
                tool_result = tool(arg) if arg else tool()
                log_info(f"Tool executed: {tool_name}")
            except Exception as e:
                log_error(f"Tool execution failed: {tool_name}", e)
                tool_result = f"Ошибка при выполнении инструмента: {str(e)}"
        
        # Generate response
        response = self.brain.generate_response(user_input, tool_result)
        
        # Add to conversation history
        self.brain.add_to_history(user_input, response)
        
        # Update memory
        self.memory_manager.increment_interactions()
        self.memory_manager.save()
        
        return response
    
    def run_interactive(self):
        """Run the agent in interactive mode."""
        print("\n" + "="*60)
        print("🤖 AI Agent started (IMPROVED VERSION)")
        print("="*60)
        print("Напиши 'помощь' для списка команд")
        print("Напиши 'выход' или 'quit' для выхода\n")
        
        log_info("AI Agent started in interactive mode")
        
        try:
            while True:
                try:
                    user_input = input("Ты: ").strip()
                    
                    # Check for exit commands
                    if user_input.lower() in ["выход", "quit", "exit", "bye"]:
                        print("AI: До свидания! 👋")
                        log_info("User exited the agent")
                        break
                    
                    if not user_input:
                        continue
                    
                    # Process input and get response
                    response = self.process_input(user_input)
                    print(f"AI: {response}\n")
                
                except KeyboardInterrupt:
                    print("\n\nAI: До встречи! 👋")
                    log_warning("Agent interrupted by user")
                    break
                except Exception as e:
                    log_error("Error in interactive loop", e)
                    print(f"AI: Произошла ошибка: {str(e)}\n")
        
        finally:
            self._save_and_exit()
    
    def run_single(self, user_input):
        """
        Run the agent with a single input (non-interactive mode).
        
        Args:
            user_input (str): User's input
            
        Returns:
            str: Agent's response
        """
        response = self.process_input(user_input)
        print(f"AI: {response}")
        self.memory_manager.save()
        return response
    
    def show_stats(self):
        """Show memory statistics."""
        stats = self.memory_manager.get_stats()
        print("\n📊 Статистика:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print()
    
    def show_help(self):
        """Show help message."""
        print(self.brain.generate_response("помощь"))
    
    def _save_and_exit(self):
        """Save memory and exit gracefully."""
        try:
            self.memory_manager.save()
            log_info("Memory saved before exit")
        except Exception as e:
            log_error("Failed to save memory on exit", e)


def main():
    """Main entry point."""
    agent = AIAgent()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            agent.show_help()
        elif sys.argv[1] == "--stats":
            agent.show_stats()
        elif sys.argv[1] == "--input":
            if len(sys.argv) > 2:
                user_input = " ".join(sys.argv[2:])
                agent.run_single(user_input)
            else:
                print("Error: --input requires an argument")
        else:
            # Treat as user input
            user_input = " ".join(sys.argv[1:])
            agent.run_single(user_input)
    else:
        # Run interactive mode
        agent.run_interactive()


if __name__ == "__main__":
    main()
