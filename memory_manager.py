import json
import os
from pathlib import Path
from datetime import datetime
from logger import log_info, log_error, log_debug


class MemoryManager:
    """Manages agent memory with persistence and backup."""
    
    def __init__(self, memory_file="memory/memory.json"):
        self.memory_file = memory_file
        self.backup_dir = Path("memory/backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.memory = self.load()
    
    def load(self):
        """
        Load memory from file.
        
        Returns:
            dict: Memory dictionary
        """
        if not os.path.exists(self.memory_file):
            log_debug("Memory file not found, creating new memory")
            return self._initialize_memory()
        
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                memory = json.load(f)
            log_info(f"Memory loaded from {self.memory_file}")
            return memory
        except json.JSONDecodeError as e:
            log_error(f"Failed to parse memory file", e)
            return self._initialize_memory()
        except Exception as e:
            log_error(f"Failed to load memory", e)
            return self._initialize_memory()
    
    def save(self):
        """
        Save memory to file with backup.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create backup before saving
            self._create_backup()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            
            # Save memory
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
            
            log_info(f"Memory saved to {self.memory_file}")
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
            
            log_debug(f"Backup created: {backup_file}")
            
            # Keep only last 10 backups
            self._cleanup_old_backups()
        except Exception as e:
            log_error(f"Failed to create backup", e)
    
    def _cleanup_old_backups(self, keep_count=10):
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backups = sorted(self.backup_dir.glob("memory_backup_*.json"))
            if len(backups) > keep_count:
                for old_backup in backups[:-keep_count]:
                    old_backup.unlink()
                    log_debug(f"Removed old backup: {old_backup}")
        except Exception as e:
            log_error(f"Failed to cleanup old backups", e)
    
    def _initialize_memory(self):
        """Initialize new memory structure."""
        memory = {
            "name": None,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "interactions_count": 0,
            "preferences": {},
            "custom_data": {}
        }
        log_info("New memory initialized")
        return memory
    
    def get(self, key, default=None):
        """Get value from memory."""
        return self.memory.get(key, default)
    
    def set(self, key, value):
        """Set value in memory."""
        self.memory[key] = value
        self.memory["last_updated"] = datetime.now().isoformat()
        log_debug(f"Memory updated: {key} = {value}")
    
    def update(self, data):
        """Update memory with multiple values."""
        self.memory.update(data)
        self.memory["last_updated"] = datetime.now().isoformat()
        log_debug(f"Memory updated with {len(data)} items")
    
    def increment_interactions(self):
        """Increment interaction counter."""
        count = self.memory.get("interactions_count", 0)
        self.memory["interactions_count"] = count + 1
    
    def get_stats(self):
        """Get memory statistics."""
        return {
            "name": self.memory.get("name"),
            "created_at": self.memory.get("created_at"),
            "last_updated": self.memory.get("last_updated"),
            "interactions_count": self.memory.get("interactions_count", 0),
        }
    
    def clear(self):
        """Clear all memory (with confirmation)."""
        log_info("Memory cleared")
        self.memory = self._initialize_memory()
        self.save()
    
    def __repr__(self):
        return f"MemoryManager({self.memory_file})"
