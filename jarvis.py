"""
IDA Jarvis Module — System Integration v1.0
Allows IDA to control your PC (Apps, Volume, Media, Files).
"""

import os
import sys
import subprocess
import platform
import webbrowser
from logger import log_info, log_error, log_warning
from main import AIAgent

class JarvisController:
    """Controls OS-level functions for IDA."""
    
    def __init__(self):
        self.os_type = platform.system()
        log_info(f"Jarvis Controller initialized for {self.os_type}")

    def open_app(self, app_name):
        """Open a system application."""
        try:
            if self.os_type == "Windows":
                os.startfile(app_name)
            elif self.os_type == "Darwin":  # macOS
                subprocess.run(["open", "-a", app_name])
            else:  # Linux
                subprocess.run(["xdg-open", app_name])
            return f"Открываю {app_name}, сэр."
        except Exception as e:
            log_error(f"Failed to open app {app_name}", e)
            return f"Не удалось открыть {app_name}."

    def search_web(self, query):
        """Open browser and search."""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Ищу «{query}» в сети."

    def system_command(self, action):
        """Control system settings."""
        if action == "shutdown":
            # Dangerous command, better ask for confirmation in real app
            return "Команда выключения получена. (Имитация)"
        elif action == "volume_up":
            # Example for macOS/Linux, Windows requires different libs
            return "Прибавляю громкость."
        return "Команда не распознана."

class IDA_Jarvis(AIAgent):
    """Extended IDA Agent with Jarvis capabilities."""
    
    def __init__(self):
        super().__init__()
        self.controller = JarvisController()
        
    def process_input(self, user_input):
        user_input = user_input.lower()
        
        # 1. Check for Jarvis-specific commands
        if "открой" in user_input:
            app = user_input.replace("открой", "").strip()
            return self.controller.open_app(app)
            
        if "найди в интернете" in user_input:
            query = user_input.replace("найди в интернете", "").strip()
            return self.controller.search_web(query)
            
        # 2. Fallback to standard IDA brain
        return super().process_input(user_input)

if __name__ == "__main__":
    print("🤖 IDA: Система 'Джарвис' активирована.")
    jarvis = IDA_Jarvis()
    jarvis.run_interactive()
