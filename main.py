"""
IDA OS v3.0 — Main entry point.
Autonomous AI Operating System with Multi-Agent Orchestration.
"""
import sys
import os
import asyncio

from logger import log_info, log_error, log_warning, log_debug
from brain import Brain
from memory_manager import MemoryManager
from core.orchestrator import Orchestrator

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
{Colors.END}{Colors.GRAY}  IDA OS v3.0 | Production-Grade AI Agent{Colors.END}
"""

class IDAOS:
    """Main IDA OS Controller."""

    def __init__(self):
        log_info("Initializing IDA OS v3.0...")
        # Initialize Memory First
        self.memory_manager = MemoryManager()
        # Initialize Brain with memory access
        self.brain = Brain(self.memory_manager.memory)
        # Link Brain back to memory for embeddings
        self.memory_manager.brain = self.brain
        # Initialize Orchestrator
        self.orchestrator = Orchestrator(self.brain, self.memory_manager)
        log_info("IDA OS initialized successfully")

    async def process_input(self, user_input: str) -> str:
        """Process user input through the Orchestrator."""
        if not user_input or not isinstance(user_input, str):
            return f"{Colors.RED}Ошибка: некорректный ввод{Colors.END}"
        
        user_input = user_input.strip()
        if not user_input:
            return f"{Colors.YELLOW}Пожалуйста, напиши что-нибудь{Colors.END}"

        log_debug(f"OS Processing: {user_input[:80]}")
        
        try:
            response = await self.orchestrator.run(user_input)
            return response
        except Exception as e:
            log_error("Orchestrator execution failed", e)
            return f"{Colors.RED}Ошибка ядра ОС: {str(e)}{Colors.END}"

    async def run_interactive(self):
        """Run the OS in interactive (REPL) mode."""
        print(ASCII_LOGO)
        print(f"{Colors.GRAY}IDA OS v3.0 готова к работе. Режим: Multi-Agent Orchestration.{Colors.END}")
        print(f"{Colors.GRAY}Напиши «выход» для завершения.{Colors.END}")
        print()

        try:
            while True:
                try:
                    user_input = input(f"{Colors.CYAN}{Colors.BOLD}╭─ Ты{Colors.END}\n{Colors.CYAN}{Colors.BOLD}╰─> {Colors.END}").strip()
                    
                    if not user_input:
                        continue
                    if user_input.lower() in ("выход", "quit", "exit", "bye"):
                        print(f"\n{Colors.GRAY}IDA OS: Завершение работы... 👋{Colors.END}")
                        break
                    
                    response = await self.process_input(user_input)
                    
                    print(f"\n{Colors.GREEN}{Colors.BOLD}IDA OS{Colors.END}")
                    print(f"{response}\n")
                    
                except KeyboardInterrupt:
                    print(f"\n\n{Colors.GRAY}IDA OS: До встречи! 👋{Colors.END}")
                    break
                except Exception as e:
                    log_error("Interactive loop error", e)
                    print(f"{Colors.RED}IDA OS: Произошла ошибка: {str(e)}{Colors.END}\n")
        finally:
            self.memory_manager.save()

async def main():
    os_instance = IDAOS()
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        response = await os_instance.process_input(user_input)
        print(f"{Colors.GREEN}{Colors.BOLD}IDA OS:{Colors.END} {response}")
    else:
        await os_instance.run_interactive()

if __name__ == "__main__":
    asyncio.run(main())
