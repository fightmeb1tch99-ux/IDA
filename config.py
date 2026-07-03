"""
Configuration file for AI Agent.

Modify these settings to customize agent behavior.
"""

# Logging configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR = "logs"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Memory configuration
MEMORY_FILE = "memory/memory.json"
MEMORY_BACKUP_DIR = "memory/backups"
MEMORY_BACKUP_COUNT = 10  # Keep last N backups

# File creation configuration
CREATED_FILES_DIR = "created_files"
MAX_FILE_SIZE = 1024 * 1024  # 1MB

# Command execution configuration
SAFE_COMMANDS = [
    "ls",      # List directory
    "pwd",     # Print working directory
    "echo",    # Print text
    "date",    # Show date/time
    "whoami",  # Show current user
    "uname",   # Show system info
]
COMMAND_TIMEOUT = 10  # seconds

# Web search configuration
SEARCH_TIMEOUT = 10  # seconds
SEARCH_API = "https://api.duckduckgo.com"

# Agent behavior
AGENT_NAME = "AI Agent"
AGENT_VERSION = "2.0"
GREETING_EMOJI = "🤖"
HELP_EMOJI = "📚"

# Feature flags
ENABLE_LOGGING = True
ENABLE_MEMORY_BACKUP = True
ENABLE_CONVERSATION_HISTORY = True
ENABLE_STATISTICS = True

# Conversation settings
MAX_CONVERSATION_HISTORY = 1000  # Keep last N interactions
RESPONSE_TIMEOUT = 30  # seconds

# Security settings
ENABLE_INPUT_VALIDATION = True
ENABLE_PATH_TRAVERSAL_PROTECTION = True
ENABLE_COMMAND_WHITELISTING = True
