# 🤖 AI Agent - Advanced Version

A sophisticated AI chatbot agent with security, logging, and advanced NLP capabilities.

## ✨ Features

### 🔒 Security Enhancements
- **Command Whitelisting**: Only safe commands can be executed
- **Path Traversal Protection**: File operations are restricted to safe directories
- **Input Validation**: All user inputs are validated and sanitized
- **Secure Command Parsing**: Uses `shlex` instead of shell injection-prone methods

### 📝 Logging & Monitoring
- **Comprehensive Logging**: All actions are logged to files and console
- **Timestamped Logs**: Each log entry includes timestamp and severity level
- **Error Tracking**: Detailed error messages with stack traces
- **Log Directory**: Logs stored in `logs/` directory with date-time naming

### 🧠 Advanced NLP
- **Regex-Based Parsing**: Flexible command recognition with multiple patterns
- **Natural Language Variations**: Recognizes different ways of saying the same command
- **Conversation History**: Tracks all interactions
- **Context Awareness**: Remembers user information

### 💾 Memory Management
- **Persistent Storage**: Memory saved to JSON files
- **Automatic Backups**: Creates backups before each save
- **Backup Rotation**: Keeps only the 10 most recent backups
- **Statistics Tracking**: Monitors interaction count and timestamps

### 🛠️ Available Tools

| Tool | Commands | Description |
|------|----------|-------------|
| **Time** | "Какое время?" | Get current time |
| **Date** | "Какая дата?" | Get current date |
| **File Creation** | "Создай файл [name]" | Create new file safely |
| **Command Execution** | "Выполни [command]" | Run safe commands (ls, pwd, echo, etc.) |
| **Web Search** | "Найди [query]" | Search the internet using DuckDuckGo |

## 📦 Installation

### Requirements
- Python 3.7+
- No external dependencies (uses only standard library)

### Setup
```bash
# Clone or navigate to the project
cd SYP-PROJECT

# Run the agent
python3 main.py
```

## 🚀 Usage

### Interactive Mode
```bash
python3 main.py
```

Start chatting with the agent. Type `помощь` for available commands.

### Single Input Mode
```bash
python3 main.py "Какое время?"
python3 main.py "Найди информацию о Python"
```

### Show Help
```bash
python3 main.py --help
```

### Show Statistics
```bash
python3 main.py --stats
```

## 📁 Project Structure

```
SYP-PROJECT/
├── main.py              # Main entry point
├── brain.py             # NLP and decision making
├── memory_manager.py    # Memory persistence
├── logger.py            # Logging configuration
├── tools/
│   └── tools.py         # Available tools
├── memory/
│   ├── memory.json      # User memory storage
│   └── backups/         # Automatic backups
├── logs/                # Application logs
├── created_files/       # Safe directory for file creation
└── README.md            # This file
```

## 🔧 Configuration

### Logging
Logs are automatically created in `logs/` directory with timestamps:
```
logs/agent_20240101_120000.log
```

### Memory
User data is stored in `memory/memory.json`:
```json
{
  "name": "User Name",
  "created_at": "2024-01-01T12:00:00",
  "last_updated": "2024-01-01T12:30:00",
  "interactions_count": 42,
  "preferences": {},
  "custom_data": {}
}
```

### Safe Commands
Only these commands can be executed:
- `ls` - List directory contents
- `pwd` - Print working directory
- `echo` - Print text
- `date` - Show date/time
- `whoami` - Show current user
- `uname` - Show system info

To add more commands, edit the `safe_commands` list in `tools/tools.py`.

## 🎯 Example Conversations

### Example 1: Getting Information
```
Ты: Какое время?
AI: 14:30:45

Ты: Какая дата?
AI: 2024-01-15
```

### Example 2: Creating Files
```
Ты: Создай файл test.txt
AI: Файл test.txt создан в папке created_files
```

### Example 3: Web Search
```
Ты: Найди информацию о машинном обучении
AI: Machine learning is a subset of artificial intelligence...
```

### Example 4: Personal Information
```
Ты: Меня зовут Иван
AI: Ок, запомнил: Иван 📝

Ты: Как меня зовут?
AI: Тебя зовут Иван
```

## 🔐 Security Considerations

### What's Protected
- ✅ Path traversal attacks blocked
- ✅ Command injection prevented
- ✅ File operations restricted to safe directory
- ✅ Input validation on all operations
- ✅ Timeout protection (10 seconds max per command)

### What You Should Know
- ⚠️ Only whitelisted commands can be executed
- ⚠️ Files are created in `created_files/` directory
- ⚠️ All actions are logged for audit trail
- ⚠️ Memory is stored locally in JSON format

## 📊 Improvements Made

### From Original Version
1. **Security**: Added input validation, command whitelisting, path traversal protection
2. **Error Handling**: Replaced bare `except:` with specific exception handling
3. **Logging**: Comprehensive logging system with file persistence
4. **NLP**: Advanced regex-based command parsing with variations
5. **Memory**: Backup system with automatic rotation
6. **Documentation**: Complete README and code comments
7. **Architecture**: Modular design with separate concerns
8. **Testing**: Better error messages and validation

## 🐛 Troubleshooting

### Memory File Corrupted
If `memory/memory.json` is corrupted:
1. Check `memory/backups/` for a recent backup
2. Restore the backup: `cp memory/backups/memory_backup_*.json memory/memory.json`
3. Run the agent again

### Logs Not Appearing
Check that `logs/` directory exists and is writable:
```bash
ls -la logs/
```

### Commands Not Executing
Check that the command is in the whitelist in `tools/tools.py`:
```python
safe_commands = ["ls", "pwd", "echo", "date", "whoami", "uname"]
```

## 📝 License

This project is part of the SYP-PROJECT repository.

## 🤝 Contributing

To improve the agent:
1. Add new tools to `tools/tools.py`
2. Add new command patterns to `brain.py`
3. Update this README
4. Test thoroughly before committing

## 📞 Support

For issues or questions:
1. Check the logs in `logs/` directory
2. Review the conversation history
3. Check memory backups if data is lost

---

**Last Updated**: 2024
**Version**: 2.0 (Improved)
