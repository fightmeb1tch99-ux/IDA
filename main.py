"""
IDA AI Agent v2.0 — Main entry point.
Инновационный динамический помощник.
"""

import sys
import os

from logger import log_info, log_error, log_warning, log_debug
from brain import Brain
from memory_manager import MemoryManager
from tools.tools import TOOLS

# Claude Code style colors
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    GRAY = '\033[90m'

ASCII_LOGO = f"""
{Colors.CYAN}{Colors.BOLD}
  ██╗██████╗  █████╗ 
  ██║██╔══██╗██╔══██╗
  ██║██║  ██║███████║
  ██║██║  ██║██╔══██║
  ██║██████╔╝██║  ██║
  ╚═╝╚═════╝ ╚═╝  ╚═╝
{Colors.END}{Colors.GRAY}  Инновационный Динамический Помощник v2.0{Colors.END}
"""

class AIAgent:
    """Main AI Agent orchestrator."""

    def __init__(self):
        log_info("Initializing IDA AI Agent v2.0...")
        self.memory_manager = MemoryManager()
        self.brain = Brain(self.memory_manager.memory)
        log_info("IDA AI Agent initialized successfully")

    def process_input(self, user_input: str) -> str:
        """Process user input and return a response."""
        if not user_input or not isinstance(user_input, str):
            return f"{Colors.RED}Ошибка: некорректный ввод{Colors.END}"
        user_input = user_input.strip()
        if not user_input:
            return f"{Colors.YELLOW}Пожалуйста, напиши что-нибудь{Colors.END}"
        if len(user_input) > 4096:
            return f"{Colors.RED}Ошибка: сообщение слишком длинное{Colors.END}"

        log_debug(f"Processing: {user_input[:80]}")

        # Decide tool
        tool_name, arg = self.brain.decide_tool(user_input)
        tool_result = None

        if tool_name:
            if tool_name == "stats":
                stats = self.memory_manager.get_stats()
                lines = [f"{Colors.BOLD}Статистика IDA:{Colors.END}"]
                for k, v in stats.items():
                    lines.append(f"  {Colors.GRAY}{k}:{Colors.END} {v}")
                tool_result = "\n".join(lines)
            elif tool_name in TOOLS:
                try:
                    tool_fn = TOOLS[tool_name]
                    tool_result = tool_fn(arg) if arg is not None else tool_fn()
                    log_info(f"Tool executed: {tool_name}")
                except Exception as e:
                    log_error(f"Tool execution failed: {tool_name}", e)
                    tool_result = f"{Colors.RED}Ошибка инструмента: {str(e)}{Colors.END}"

        response = self.brain.generate_response(user_input, tool_result)
        self.brain.add_to_history(user_input, response)
        self.memory_manager.increment_interactions()
        self.memory_manager.save()
        return response

    def run_interactive(self):
        """Run the agent in interactive (REPL) mode."""
        print(ASCII_LOGO)
        print(f"{Colors.GRAY}Напиши {Colors.END}{Colors.BOLD}«помощь»{Colors.END}{Colors.GRAY} для списка команд{Colors.END}")
        print(f"{Colors.GRAY}Напиши {Colors.END}{Colors.BOLD}«выход»{Colors.END}{Colors.GRAY} для завершения{Colors.END}")
        print()
        log_info("IDA started in interactive mode")

        try:
            while True:
                try:
                    # Claude-like prompt
                    user_input = input(f"{Colors.CYAN}{Colors.BOLD}╭─ Ты{Colors.END}\n{Colors.CYAN}{Colors.BOLD}╰─> {Colors.END}").strip()
                    
                    if not user_input:
                        continue
                    if user_input.lower() in ("выход", "quit", "exit", "bye", "пока"):
                        print(f"\n{Colors.GRAY}IDA: До свидания! 👋{Colors.END}")
                        log_info("User exited")
                        break
                    
                    response = self.process_input(user_input)
                    
                    # Claude-like response styling
                    print(f"\n{Colors.GREEN}{Colors.BOLD}IDA{Colors.END}")
                    print(f"{response}\n")
                    
                except KeyboardInterrupt:
                    print(f"\n\n{Colors.GRAY}IDA: До встречи! 👋{Colors.END}")
                    log_warning("Interrupted by user")
                    break
                except Exception as e:
                    log_error("Interactive loop error", e)
                    print(f"{Colors.RED}IDA: Произошла ошибка: {str(e)}{Colors.END}\n")
        finally:
            self._save_and_exit()

    def run_single(self, user_input: str) -> str:
        """Process a single input (non-interactive mode)."""
        response = self.process_input(user_input)
        print(f"{Colors.GREEN}{Colors.BOLD}IDA:{Colors.END} {response}")
        self.memory_manager.save()
        return response

    def show_stats(self):
        """Print memory statistics."""
        stats = self.memory_manager.get_stats()
        print(f"\n{Colors.BOLD}Статистика IDA:{Colors.END}")
        for key, value in stats.items():
            print(f"  {Colors.GRAY}{key}:{Colors.END} {value}")
        print()

    def show_help(self):
        """Print help message."""
        print(self.brain.generate_response("помощь"))

    def _save_and_exit(self):
        try:
            self.memory_manager.save()
            log_info("Memory saved on exit")
        except Exception as e:
            log_error("Failed to save memory on exit", e)

def main():
    agent = AIAgent()
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("--help", "-h"):
            agent.show_help()
        elif arg == "--stats":
            agent.show_stats()
        elif arg == "--input":
            if len(sys.argv) > 2:
                agent.run_single(" ".join(sys.argv[2:]))
            else:
                print("Ошибка: --input требует аргумент")
                sys.exit(1)
        else:
            agent.run_single(" ".join(sys.argv[1:]))
    else:
        agent.run_interactive()

if __name__ == "__main__":
    main()
