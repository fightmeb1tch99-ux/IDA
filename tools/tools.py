import datetime
import subprocess
import urllib.request
import json
import os
import shlex
from pathlib import Path
from logger import log_info, log_error, log_warning, log_debug


def get_time():
    """Get current time in HH:MM:SS format."""
    try:
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        log_debug(f"Time requested: {time_str}")
        return time_str
    except Exception as e:
        log_error("Failed to get time", e)
        return "Ошибка при получении времени"


def get_date():
    """Get current date in YYYY-MM-DD format."""
    try:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        log_debug(f"Date requested: {date_str}")
        return date_str
    except Exception as e:
        log_error("Failed to get date", e)
        return "Ошибка при получении даты"


def create_file(filename):
    """
    Create an empty file with validation.
    
    Args:
        filename (str): Name of the file to create
        
    Returns:
        str: Success or error message
    """
    if not filename or not isinstance(filename, str):
        log_warning(f"Invalid filename provided: {filename}")
        return "Ошибка: некорректное имя файла"
    
    # Prevent path traversal attacks
    filename = filename.strip()
    if ".." in filename or filename.startswith("/"):
        log_warning(f"Potential path traversal attempt: {filename}")
        return "Ошибка: недопустимый путь"
    
    try:
        # Create file in safe directory
        safe_path = Path("created_files") / filename
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write("")
        
        log_info(f"File created: {safe_path}")
        return f"Файл {filename} создан в папке created_files"
    except Exception as e:
        log_error(f"Failed to create file {filename}", e)
        return f"Ошибка при создании файла: {str(e)}"


def run_command(command):
    """
    Execute a shell command safely with validation.
    
    Args:
        command (str): Command to execute
        
    Returns:
        str: Command output or error message
    """
    if not command or not isinstance(command, str):
        log_warning("Invalid command provided")
        return "Ошибка: некорректная команда"
    
    command = command.strip()
    
    # Whitelist of safe commands
    safe_commands = ["ls", "pwd", "echo", "date", "whoami", "uname"]
    cmd_name = command.split()[0] if command else ""
    
    if cmd_name not in safe_commands:
        log_warning(f"Potentially unsafe command attempted: {cmd_name}")
        return f"Ошибка: команда '{cmd_name}' не разрешена. Разрешённые: {', '.join(safe_commands)}"
    
    try:
        # Use shlex to safely parse command
        args = shlex.split(command)
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        
        if result.returncode != 0:
            log_warning(f"Command failed: {command}, stderr: {result.stderr}")
            return f"Ошибка выполнения: {result.stderr}" if result.stderr else "Готово с ошибкой"
        
        log_info(f"Command executed successfully: {command}")
        return result.stdout.strip() if result.stdout else "Готово"
    
    except subprocess.TimeoutExpired:
        log_error(f"Command timeout: {command}")
        return "Ошибка: команда выполнялась слишком долго"
    except Exception as e:
        log_error(f"Failed to execute command {command}", e)
        return f"Ошибка: {str(e)}"


def web_search(query):
    """
    Search the web using DuckDuckGo API.
    
    Args:
        query (str): Search query
        
    Returns:
        str: Search result or error message
    """
    if not query or not isinstance(query, str):
        log_warning("Invalid search query provided")
        return "Ошибка: некорректный запрос"
    
    query = query.strip()
    
    try:
        # Encode query properly
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json"
        
        # Add timeout and user-agent
        headers = {"User-Agent": "AIAgent/1.0"}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        # Try to get abstract text
        abstract = data.get("AbstractText")
        if abstract:
            log_info(f"Search successful for: {query}")
            return abstract
        
        # Try related topics
        related = data.get("RelatedTopics", [])
        if related and isinstance(related, list) and len(related) > 0:
            result = related[0].get("Text", "Нет точного ответа")
            log_info(f"Search successful (related) for: {query}")
            return result
        
        log_warning(f"No results found for: {query}")
        return "Ничего не найдено 🤷"
    
    except urllib.error.URLError as e:
        log_error(f"Network error during search for: {query}", e)
        return f"Ошибка интернета: проверьте соединение"
    except Exception as e:
        log_error(f"Failed to search for: {query}", e)
        return f"Ошибка поиска: {str(e)}"


# Tool registry
TOOLS = {
    "time": get_time,
    "date": get_date,
    "create_file": create_file,
    "run": run_command,
    "search": web_search,
}


def get_available_tools():
    """Get list of available tools with descriptions."""
    return {
        "time": "Получить текущее время",
        "date": "Получить текущую дату",
        "create_file": "Создать новый файл",
        "run": "Выполнить команду (только безопасные)",
        "search": "Поиск в интернете",
    }
