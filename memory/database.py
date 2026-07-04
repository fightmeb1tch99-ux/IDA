"""
SQLite Database Manager for IDA OS
Handles structured memory, logs, and user data.
"""
import sqlite3
import json
from datetime import datetime
from logger import log_info, log_error

class DatabaseManager:
    def __init__(self, db_path="memory/ida_os.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table for long-term interactions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    user_input TEXT,
                    agent_response TEXT,
                    thought_process TEXT,
                    metadata TEXT
                )
            ''')
            
            # Table for tasks and plans
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT,
                    description TEXT,
                    plan TEXT,
                    created_at DATETIME
                )
            ''')
            
            conn.commit()
            conn.close()
            log_info("Database initialized successfully")
        except Exception as e:
            log_error("Failed to initialize database", e)

    def add_interaction(self, user_input, response, thought="", metadata=None):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO interactions (timestamp, user_input, agent_response, thought_process, metadata) VALUES (?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), user_input, response, thought, json.dumps(metadata or {}))
            )
            conn.commit()
            conn.close()
        except Exception as e:
            log_error("Failed to add interaction to DB", e)

    def get_recent_history(self, limit=10):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT user_input, agent_response FROM interactions ORDER BY id DESC LIMIT ?", (limit,))
            history = cursor.fetchall()
            conn.close()
            return history
        except Exception as e:
            log_error("Failed to fetch history from DB", e)
            return []
