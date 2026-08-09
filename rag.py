"""
IDA RAG Module — Knowledge Base System
Allows IDA to read and search through local documents (PDF, TXT, MD).
Simple keyword search now. Ready for embeddings upgrade later.
"""

import os
from pathlib import Path
from logger import log_info, log_error, log_warning

try:
    from pypdf import PdfReader
    _PDF_AVAILABLE = True
except ImportError:
    try:
        import PyPDF2
        PdfReader = PyPDF2.PdfReader
        _PDF_AVAILABLE = True
    except ImportError:
        _PDF_AVAILABLE = False
        log_warning("pypdf / PyPDF2 not installed — PDF support disabled")


class KnowledgeBase:
    def __init__(self, docs_dir="knowledge"):
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(exist_ok=True)
        self.documents = []
        self._loaded = False

    def load_documents(self, force: bool = False):
        """Load all TXT, MD and PDF files from the knowledge directory."""
        if self._loaded and not force:
            return

        self.documents = []
        for file_path in self.docs_dir.rglob("*"):
            if not file_path.is_file():
                continue
            suffix = file_path.suffix.lower()
            if suffix in (".txt", ".md"):
                self._load_text(file_path)
            elif suffix == ".pdf" and _PDF_AVAILABLE:
                self._load_pdf(file_path)

        self._loaded = True
        log_info(f"Knowledge Base: loaded {len(self.documents)} chunks from {self.docs_dir}")

    def _load_text(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # Chunk by paragraphs, keep reasonable size
            chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 30]
            for chunk in chunks:
                self.documents.append({"text": chunk, "source": path.name})
        except Exception as e:
            log_error(f"Error loading text {path.name}", e)

    def _load_pdf(self, path: Path):
        try:
            reader = PdfReader(str(path))
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                text = text.strip()
                if len(text) > 30:
                    self.documents.append({
                        "text": text,
                        "source": f"{path.name} (стр. {i+1})"
                    })
        except Exception as e:
            log_error(f"Error loading PDF {path.name}", e)

    def search(self, query: str, top_k: int = 3) -> str:
        """Simple keyword-based search. Upgrade to embeddings later."""
        self.load_documents()
        if not self.documents:
            return "База знаний пуста. Положи .txt / .md / .pdf файлы в папку knowledge/"

        query_words = [w for w in query.lower().split() if len(w) > 2]
        if not query_words:
            return "Слишком короткий запрос для поиска."

        results = []
        for doc in self.documents:
            text_lower = doc["text"].lower()
            score = sum(1 for word in query_words if word in text_lower)
            if score > 0:
                results.append((score, doc))

        results.sort(key=lambda x: x[0], reverse=True)

        if not results:
            return "В базе знаний ничего не найдено по этому запросу."

        formatted = []
        for score, doc in results[:top_k]:
            preview = doc["text"][:500] + ("..." if len(doc["text"]) > 500 else "")
            formatted.append(f"--- Источник: {doc['source']} (релевантность: {score}) ---\n{preview}")

        return "\n\n".join(formatted)


# Global instance
kb = KnowledgeBase()


def ask_knowledge(query: str) -> str:
    """Tool function to search the knowledge base."""
    return kb.search(query)
