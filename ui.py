"""
UI Module for IDA - ASCII Loading Animation and Interactive Code Editor
Создатель: Григорьев Айтал Григорьевич (@Mareioak)
"""

import time
import sys
import os
from typing import Optional

class DonutLoader:
    """ASCII Donut Loading Animation"""
    
    DONUT_FRAMES = [
        """
        🍩
        """,
        """
         🍩
        """,
        """
          🍩
        """,
        """
           🍩
        """,
        """
            🍩
        """,
        """
           🍩
        """,
        """
          🍩
        """,
        """
         🍩
        """,
    ]
    
    LOADING_BARS = [
        "▁▂▃▄▅▆▇█",
        "█▁▂▃▄▅▆▇",
        "▇█▁▂▃▄▅▆",
        "▆▇█▁▂▃▄▅",
        "▅▆▇█▁▂▃▄",
        "▄▅▆▇█▁▂▃",
        "▃▄▅▆▇█▁▂",
        "▂▃▄▅▆▇█▁",
    ]
    
    @staticmethod
    def show_loading(message: str = "IDA загружается", duration: float = 3.0):
        """Show ASCII donut loading animation"""
        start_time = time.time()
        frame = 0
        
        while time.time() - start_time < duration:
            sys.stdout.write('\r')
            sys.stdout.write(f"{DonutLoader.DONUT_FRAMES[frame % len(DonutLoader.DONUT_FRAMES)].strip()}")
            sys.stdout.write(f" {message} {DonutLoader.LOADING_BARS[frame % len(DonutLoader.LOADING_BARS)]}")
            sys.stdout.flush()
            
            time.sleep(0.1)
            frame += 1
        
        sys.stdout.write('\r')
        sys.stdout.write(" " * 60)
        sys.stdout.write('\r')
        sys.stdout.flush()
    
    @staticmethod
    def show_progress_donut(current: int, total: int, message: str = "Обработка"):
        """Show progress with donut animation"""
        percent = (current / total) * 100
        bar_length = 30
        filled = int(bar_length * current / total)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        frame = current % len(DonutLoader.DONUT_FRAMES)
        donut = DonutLoader.DONUT_FRAMES[frame].strip()
        
        sys.stdout.write('\r')
        sys.stdout.write(f"{donut} {message}: [{bar}] {percent:.0f}%")
        sys.stdout.flush()


class CodeEditor:
    """Interactive Code Editor for Termux"""
    
    def __init__(self, filename: str = "code.py"):
        self.filename = filename
        self.lines = []
        self.current_line = 0
    
    def load_file(self) -> bool:
        """Load existing file if it exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.lines = f.readlines()
                return True
            except Exception as e:
                print(f"❌ Ошибка при загрузке файла: {e}")
                return False
        return False
    
    def save_file(self) -> bool:
        """Save code to file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.writelines(self.lines)
            print(f"✅ Файл сохранён: {self.filename}")
            return True
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")
            return False
    
    def display_editor(self):
        """Display the editor interface"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("=" * 60)
        print(f"📝 IDA Code Editor - {self.filename}")
        print("=" * 60)
        print("\n📋 Команды:")
        print("  :q  - Выход без сохранения")
        print("  :w  - Сохранить файл")
        print("  :wq - Сохранить и выход")
        print("  :n  - Новая строка")
        print("  :d  - Удалить строку")
        print("  :l  - Показать все строки")
        print("\n" + "=" * 60)
        print()
        
        self.show_lines()
    
    def show_lines(self):
        """Display all lines with numbers"""
        if not self.lines:
            print("(пусто)")
        else:
            for i, line in enumerate(self.lines, 1):
                print(f"{i:3d} | {line.rstrip()}")
        print()
    
    def run_editor(self):
        """Run the interactive editor"""
        self.load_file()
        
        while True:
            self.display_editor()
            
            try:
                user_input = input(">>> ").strip()
                
                if user_input == ":q":
                    print("Выход без сохранения.")
                    break
                
                elif user_input == ":w":
                    self.save_file()
                    input("Нажми Enter для продолжения...")
                
                elif user_input == ":wq":
                    self.save_file()
                    break
                
                elif user_input == ":l":
                    print("\n📄 Содержимое файла:")
                    self.show_lines()
                    input("Нажми Enter для продолжения...")
                
                elif user_input == ":n":
                    line = input("Введи новую строку: ")
                    self.lines.append(line + "\n")
                    print(f"✅ Строка добавлена (всего {len(self.lines)})")
                    time.sleep(1)
                
                elif user_input == ":d":
                    if self.lines:
                        line_num = input(f"Какую строку удалить? (1-{len(self.lines)}): ")
                        try:
                            idx = int(line_num) - 1
                            if 0 <= idx < len(self.lines):
                                del self.lines[idx]
                                print("✅ Строка удалена")
                            else:
                                print("❌ Неверный номер строки")
                        except ValueError:
                            print("❌ Введи число")
                    else:
                        print("❌ Файл пуст")
                    time.sleep(1)
                
                elif user_input.startswith(":"):
                    print(f"❌ Неизвестная команда: {user_input}")
                    time.sleep(1)
                
                elif user_input:
                    self.lines.append(user_input + "\n")
                    print(f"✅ Добавлено (строк: {len(self.lines)})")
                    time.sleep(0.5)
            
            except KeyboardInterrupt:
                print("\n\n⚠️ Прервано пользователем")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                time.sleep(1)


class TermuxUI:
    """Main UI for Termux IDA"""
    
    @staticmethod
    def show_banner():
        """Show IDA banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  🤖 IDA v 0.1 - Инновационный динамический помощник     ║
║                                                           ║
║  Создатель: Григорьев Айтал Григорьевич (@Mareioak)     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    @staticmethod
    def show_menu():
        """Show main menu"""
        print("\n📌 Выбери действие:")
        print("  1️⃣  - Общаться с IDA")
        print("  2️⃣  - Открыть редактор кода")
        print("  3️⃣  - Показать справку")
        print("  4️⃣  - Выход")
        print()
        return input(">>> ").strip()
    
    @staticmethod
    def show_help():
        """Show help"""
        help_text = """
╔════════════════════════════════════════════════════════════╗
║                    📚 СПРАВКА IDA v 0.1                   ║
╚════════════════════════════════════════════════════════════╝

⏰ ВРЕМЯ И ДАТА:
  "Какое время?" → текущее время
  "Какая дата?" → текущая дата

📁 РАБОТА С ФАЙЛАМИ:
  "Создай файл [имя]" → создать файл
  "Удали файл [имя]" → удалить файл

🔍 ПОИСК:
  "Найди [запрос]" → поиск в интернете

⚙️ КОМАНДЫ:
  "Выполни [команда]" → запустить команду
  "--help" → эта справка
  "--stats" → статистика

👤 ЛИЧНОЕ:
  "Меня зовут [имя]" → сохранить имя
  "Как меня зовут?" → узнать имя

💬 ПРОСТО ОБЩАЙСЯ:
  Напиши любой текст и IDA ответит!

        """
        print(help_text)


def main():
    """Main entry point for UI"""
    TermuxUI.show_banner()
    
    while True:
        choice = TermuxUI.show_menu()
        
        if choice == "1":
            print("\n💬 Режим общения с IDA")
            print("(введи 'выход' для возврата в меню)\n")
            break  # Вернёмся в main.py для общения
        
        elif choice == "2":
            print("\n📝 Открываю редактор кода...\n")
            DonutLoader.show_loading("Инициализация редактора", 1.5)
            editor = CodeEditor("my_code.py")
            editor.run_editor()
        
        elif choice == "3":
            TermuxUI.show_help()
            input("\nНажми Enter для продолжения...")
        
        elif choice == "4":
            print("\n👋 До встречи!")
            sys.exit(0)
        
        else:
            print("❌ Неверный выбор")
            time.sleep(1)


if __name__ == "__main__":
    main()
