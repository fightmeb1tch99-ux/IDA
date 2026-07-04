"""
IDA RAG Module — Knowledge Base System
Allows IDA to read and search through local documents (PDF, TXT).
"""

import os
from pathlib import Path
import PyPDF2
from logger import log_info, log_error

class KnowledgeBase:
    def __init__(self, docs_dir="knowledge"):
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(exist_ok=True)
        self.documents = []

    def load_documents(self):
        """Load all TXT and PDF files from the knowledge directory."""
        self.documents = []
        for file_path in self.docs_dir.glob("*"):
            if file_path.suffix.lower() == ".txt":
                self._load_txt(file_path)
            elif file_path.suffix.lower() == ".pdf":
                self._load_pdf(file_path)
        log_info(f"Loaded {len(self.documents)} document chunks into Knowledge Base.")

    def _load_txt(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                # Simple chunking by paragraphs
                chunks = content.split("\n\n")
                for chunk in chunks:
                    if len(chunk.strip()) > 20:
                        self.documents.append({"text": chunk.strip(), "source": path.name})
        except Exception as e:
            log_error(f"Error loading TXT {path.name}", e)

    def _load_pdf(self, path):
        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text and len(text.strip()) > 20:
                        self.documents.append({"text": text.strip(), "source": f"{path.name} (page {i+1})"})
        except Exception as e:
            log_error(f"Error loading PDF {path.name}", e)

    def search(self, query: str, top_k=3):
        """Simple keyword-based search (can be upgraded to embeddings later)."""
        if not self.documents:
            return "База знаний пуста."
        
        query_words = query.lower().split()
        results = []
        
        for doc in self.documents:
            score = sum(1 for word in query_words if word in doc["text"].lower())
            if score > 0:
                results.append((score, doc))
        
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        
        if not results:
            return "В базе знаний ничего не найдено."
        
        formatted_results = []
        for score, doc in results[:top_k]:
            formatted_results.append(f"--- Источник: {doc['source']} ---\n{doc['text']}")
        
        return "\n\n".join(formatted_results)

# Global instance
kb = KnowledgeBase()

def ask_knowledge(query: str):
    """Tool function to search the knowledge base."""
    kb.load_documents() # Refresh docs on search
    return kb.search(query)
