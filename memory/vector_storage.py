"""
Vector Storage for IDA OS
Handles semantic search using OpenAI embeddings and local storage.
"""
import os
import json
import numpy as np
from typing import List, Dict, Any
from logger import log_info, log_error

class VectorStorage:
    def __init__(self, storage_path="memory/vector/embeddings.json"):
        self.storage_path = storage_path
        self.embeddings_data = []
        self._load_storage()

    def _load_storage(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.embeddings_data = json.load(f)
                log_info(f"Loaded {len(self.embeddings_data)} embeddings from storage")
            except Exception as e:
                log_error("Failed to load vector storage", e)
                self.embeddings_data = []

    def _save_storage(self):
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.embeddings_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log_error("Failed to save vector storage", e)

    def add_text(self, text: str, embedding: List[float], metadata: Dict[str, Any] = None):
        """Add text and its embedding to the storage."""
        self.embeddings_data.append({
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        })
        self._save_storage()

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Perform semantic search using cosine similarity."""
        if not self.embeddings_data:
            return []

        similarities = []
        query_vec = np.array(query_embedding)

        for item in self.embeddings_data:
            item_vec = np.array(item["embedding"])
            # Cosine similarity: (A dot B) / (||A|| * ||B||)
            similarity = np.dot(query_vec, item_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(item_vec))
            similarities.append((similarity, item))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        return [item for _, item in similarities[:top_k]]
