"""
Memory Manager for IDA OS v3.0
Integrates SQLite for structured data and VectorStorage for semantic search.
Maintains backward compatibility for basic memory functions.
"""
import json
import os
from pathlib import Path
from datetime import datetime
from memory.database import DatabaseManager
from memory.vector_storage import VectorStorage
from logger import log_info, log_error, log_debug

class MemoryManager:
    """Manages agent memory with persistence, SQLite, and Vector Search."""
    
    def __init__(self, memory_file="memory/memory.json", brain=None):
        self.memory_file = memory_file
        self.backup_dir = Path("memory/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.brain = brain
        
        # New v3.0 storage systems
        self.db = DatabaseManager()
        self.vector = VectorStorage()
        
        # Legacy JSON memory for simple key-value storage
        self.memory = self.load()
        log_info("MemoryManager v3.0 initialized")

    def load(self):
        """Load legacy JSON memory from file."""
        if not os.path.exists(self.memory_file):
            log_debug("Memory file not found, creating new memory")
            return self._initialize_memory()
        
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                memory = json.load(f)
            log_info(f"Memory loaded from {self.memory_file}")
            return memory
        except Exception as e:
            log_error(f"Failed to load memory", e)
            return self._initialize_memory()

    def save(self):
        """Save legacy JSON memory to file with backup."""
        try:
            self._create_backup()
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            log_error(f"Failed to save memory", e)
            return False

    def _create_backup(self):
        """Create a backup of current memory file."""
        if not os.path.exists(self.memory_file):
            return
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"memory_backup_{timestamp}.json"
            with open(self.memory_file, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Failed to create backup", e)

    def _initialize_memory(self):
        """Initialize new memory structure."""
        return {
            "name": None,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "interactions_count": 0,
            "preferences": {},
            "custom_data": {}
        }

    # --- v3.0 Enhanced Memory Features ---

    def save_interaction(self, user_input, response, thought="", metadata=None):
        """Save interaction to both SQLite and Vector Storage."""
        # Save to SQLite
        self.db.add_interaction(user_input, response, thought, metadata)
        
        # Save to Vector Storage for semantic search
        if self.brain:
            text_to_embed = f"User: {user_input}\nIDA: {response}"
            embedding = self.brain.get_embedding(text_to_embed)
            if embedding:
                self.vector.add_text(text_to_embed, embedding, {
                    "timestamp": datetime.now().isoformat(),
                    "type": "interaction"
                })
        
        # Legacy increment
        self.increment_interactions()
        self.save()

    def search_memory(self, query, top_k=3):
        """Search memory semantically."""
        if not self.brain:
            return []
        query_embedding = self.brain.get_embedding(query)
        if not query_embedding:
            return []
        return self.vector.search(query_embedding, top_k)

    def get_context(self, query=None):
        """Get recent history and relevant semantic context."""
        recent = self.db.get_recent_history(limit=5)
        semantic = []
        if query:
            semantic = self.search_memory(query, top_k=2)
            
        return {
            "recent_history": recent,
            "semantic_context": [s["text"] for s in semantic]
        }

    # --- Legacy Compatibility Methods ---
    def get(self, key, default=None):
        return self.memory.get(key, default)
    
    def set(self, key, value):
        self.memory[key] = value
        self.memory["last_updated"] = datetime.now().isoformat()
        self.save()
    
    def increment_interactions(self):
        count = self.memory.get("interactions_count", 0)
        self.memory["interactions_count"] = count + 1
