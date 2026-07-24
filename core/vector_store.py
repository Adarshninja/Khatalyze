
"""
core/vector_store.py

FAISS vector store for FinSight AI.
"""

from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # cosine (normalized vectors)
        self.chunks = []

    def add_embeddings(self, embeddings: np.ndarray, chunks: list[dict]):
        embeddings = np.asarray(embeddings, dtype="float32")

        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D numpy array.")

        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension mismatch. "
                f"Expected {self.dimension}, got {embeddings.shape[1]}"
            )

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        query_embedding = np.asarray(query_embedding, dtype="float32").reshape(1, -1)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or idx >= len(self.chunks):
                continue

            results.append({
                "score": float(score),
                "chunk_id": idx,
                "section": self.chunks[idx].get("section"),
                "text": self.chunks[idx].get("text"),
            })

        return results

    def save(self, directory: str = "data/vector_db"):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(directory / "index.faiss"))

        with open(directory / "chunks.json", "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, directory: str = "data/vector_db"):
        directory = Path(directory)

        index = faiss.read_index(str(directory / "index.faiss"))

        with open(directory / "chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

        store = cls(index.d)
        store.index = index
        store.chunks = chunks
        return store

    @property
    def size(self):
        return self.index.ntotal

    def __len__(self):
        return self.index.ntotal
