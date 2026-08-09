"""
Configuration file for IDA AI Agent v2.0
Modify these settings to customize agent behavior.
"""

import os

# LLM / OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

# Available models: gpt-4o-mini (balanced), gpt-4o (smart)
LLM_MODEL = os.getenv("IDA_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 1024
EMBEDDING_MODEL = "text-embedding-3-small"

# Logging configuration
LOG_LEVEL = os.getenv("IDA_LOG_LEVEL", "INFO")
LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Memory configuration
MEMORY_FILE = "memory/memory.json"
MEMORY_BACKUP_DIR = "memory/backups"
MEMORY_BACKUP_COUNT = 10

# File creation configuration
CREATED_FILES_DIR = "created_files"
MAX_FILE_SIZE = 1024 * 1024  # 1 MB

# Command execution configuration
SAFE_COMMANDS = [
    "ls", "pwd", "echo", "date", "whoami", "uname", "uptime", "df", "free",
]
COMMAND_TIMEOUT = 10  # seconds

# Web search configuration
SEARCH_TIMEOUT = 10  # seconds
SEARCH_API = "https://api.duckduckgo.com"

# Agent identity
AGENT_NAME = "IDA"
AGENT_VERSION = "3.0"
AGENT_FULL_NAME = "Инновационный динамический помощник"
GREETING_EMOJI = "🤖"
HELP_EMOJI = "📚"

# Feature flags
ENABLE_LOGGING = True
ENABLE_MEMORY_BACKUP = True
ENABLE_CONVERSATION_HISTORY = True
ENABLE_STATISTICS = True
ENABLE_WEATHER = True
ENABLE_CALCULATOR = True
ENABLE_NOTES = True

# Conversation settings
MAX_CONVERSATION_HISTORY = 1000
CONTEXT_WINDOW = 10
RESPONSE_TIMEOUT = 30

# Security settings
ENABLE_INPUT_VALIDATION = True
ENABLE_PATH_TRAVERSAL_PROTECTION = True
ENABLE_COMMAND_WHITELISTING = True
MAX_INPUT_LENGTH = 4096
