"""Persistent memory and vector store for the self‑editing agent.

This module provides classes for storing conversational history and code
embeddings.  A simple SQLite database keeps track of messages, rationales
and other metadata.  Optionally, a FAISS index can be used to perform
similarity search over text embeddings (e.g. to recall relevant past
discussions or code snippets).
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import logging

try:
    import faiss  # type: ignore
except ImportError:  # pragma: no cover
    faiss = None  # type: ignore

from .. import config
from .tools import embed_texts


logger = logging.getLogger(__name__)


class Memory:
    """SQLite‑backed memory for storing messages and embeddings."""

    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = Path(db_path or config.MEMORY_DB_PATH)
        self.conn = sqlite3.connect(self.db_path)
        self._ensure_tables()
        # Lazy initialisation of the FAISS index; built when first embedding is added
        self.index = None
        self.vectors: List[List[float]] = []
        self.vector_texts: List[str] = []

    def _ensure_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT
            );
            """
        )
        self.conn.commit()

    def append_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Append a message with optional metadata.

        :param role: speaker role, e.g. "user", "assistant", "system"
        :param content: text content of the message
        :param metadata: optional dictionary of metadata; will be stored as JSON
        """
        meta_json = json.dumps(metadata or {})
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO messages (role, content, metadata) VALUES (?, ?, ?)",
            (role, content, meta_json),
        )
        self.conn.commit()

    def all_messages(self) -> List[Tuple[int, str, str, Dict[str, Any]]]:
        """Return all stored messages as a list of tuples.

        Each tuple has the form `(id, role, content, metadata)`.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id, role, content, metadata FROM messages ORDER BY id ASC")
        rows = cur.fetchall()
        result: List[Tuple[int, str, str, Dict[str, Any]]] = []
        for row in rows:
            msg_id, role, content, meta_json = row
            try:
                metadata = json.loads(meta_json) if meta_json else {}
            except Exception:
                metadata = {}
            result.append((msg_id, role, content, metadata))
        return result

    def store_embeddings(self, texts: Iterable[str]) -> None:
        """Compute and store embeddings for the given texts.

        This method uses the `embed_texts` function to compute embedding
        vectors.  Embeddings are accumulated in memory and optionally added to
        a FAISS index for similarity search.

        :param texts: an iterable of strings to embed
        """
        try:
            embeddings = embed_texts(texts)
        except NotImplementedError:
            logger.warning("Embeddings not available; skipping storing embeddings")
            return
        for text, embedding in zip(texts, embeddings):
            self.vectors.append(embedding)
            self.vector_texts.append(text)
        if faiss is not None:
            dim = len(self.vectors[0])
            if self.index is None:
                self.index = faiss.IndexFlatL2(dim)
            # FAISS requires float32 arrays
            import numpy as np  # type: ignore

            arr = np.array(embeddings, dtype="float32")
            self.index.add(arr)
        else:
            logger.debug("faiss not installed; embeddings stored but similarity search disabled")

    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """Perform a simple similarity search over stored embeddings.

        If FAISS and embeddings are available, this will return the top `k`
        nearest texts along with distances.  Otherwise, an empty list is
        returned.
        """
        if faiss is None or self.index is None or not self.vectors:
            return []
        try:
            query_embedding = embed_texts([query])[0]
        except NotImplementedError:
            return []
        import numpy as np  # type: ignore

        xq = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(xq, k)
        results: List[Tuple[str, float]] = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.vector_texts):
                results.append((self.vector_texts[idx], float(dist)))
        return results


__all__ = ["Memory"]
