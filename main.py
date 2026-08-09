#!/usr/bin/env python3
"""
IDA — Инновационный Динамический AI-помощник
Main entry point
"""

import sys
import argparse
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from logger import log_info, log_error
from brain import Brain
from memory_manager import MemoryManager


def print_banner():
    print("""
╔════════════════════════════════════════════════════════════════╗
║   ██╗██████╗  █████╗                                           ║
║   ██║██╔══██╗██╔══██╗                                          ║
║   ██║██║  ██║███████║                                          ║
║   ██║██║  ██║██╔══██║                                          ║
║   ██║██████╔╝██║  ██║                                          ║
║   ╚═╝╚═════╝ ╚═╝  ╚═╝                                          ║
║                                                                ║
║     Инновационный Динамический Помощник  •  v4.1               ║
╚════════════════════════════════════════════════════════════════╝
    """)


def handle_input(brain: Brain, user_input: str) -> str:
    """Единая точка обработки пользовательского ввода."""
    from tools.tools import TOOLS

    tool_name, arg = brain.decide_tool(user_input)

    tool_result = None
    if tool_name and tool_name in TOOLS:
        try:
            tool_fn = TOOLS[tool_name]
            if arg is not None:
                tool_result = tool_fn(arg)
            else:
                tool_result = tool_fn()
        except TypeError:
            try:
                tool_result = TOOLS[tool_name](arg) if arg else TOOLS[tool_name]()
            except Exception as e:
                tool_result = f"Ошибка инструмента: {e}"
        except Exception as e:
            tool_result = f"Ошибка при выполнении: {e}"

    response = brain.generate_response(user_input, tool_result)
    brain.add_to_history(user_input, response)

    # Сохраняем память
    try:
        from memory_manager import MemoryManager
        MemoryManager().save(brain.memory)
    except Exception:
        pass

    return response


def interactive_mode(brain: Brain):
    """Запуск интерактивного режима."""
    print_banner()
    print("IDA готов. Пиши команду или вопрос (или 'выход' / 'exit').\n")

    while True:
        try:
            user_input = input("Ты > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("выход", "exit", "quit", "q"):
                print("До связи, брат.")
                break

            response = handle_input(brain, user_input)
            print(f"\nIDA > {response}\n")

        except KeyboardInterrupt:
            print("\n\nПрервано. До связи!")
            break
        except Exception as e:
            log_error("Ошибка в интерактивном режиме", e)
            print(f"[Ошибка] {e}")


def single_command(brain: Brain, command: str):
    """Выполнить одну команду и выйти."""
    response = handle_input(brain, command)
    print(response)


def main():
    parser = argparse.ArgumentParser(description="IDA — Инновационный Динамический AI-помощник")
    parser.add_argument("command", nargs="?", help="Одна команда для выполнения")
    parser.add_argument("--stats", action="store_true", help="Показать статистику")
    parser.add_argument("--version", action="store_true", help="Показать версию")
    args = parser.parse_args()

    if args.version:
        print("IDA v4.1")
        return

    memory_mgr = MemoryManager()
    brain = Brain(memory_mgr.load())

    if args.stats:
        print("Статистика IDA:")
        print("  (в разработке)")
        return

    if args.command:
        single_command(brain, args.command)
    else:
        interactive_mode(brain)


if __name__ == "__main__":
    main()
