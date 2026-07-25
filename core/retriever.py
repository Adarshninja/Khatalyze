from __future__ import annotations

from pathlib import Path

from sentence_transformers import SentenceTransformer

from core.vector_store import VectorStore


class Retriever:

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(
        self,
        vector_store: VectorStore | str | Path,
    ):

        if isinstance(
            vector_store,
            (str, Path)
        ):
            self.vector_store = VectorStore.load(
                vector_store
            )
        else:
            self.vector_store = vector_store

        self.model = SentenceTransformer(
            self.MODEL_NAME
        )

    def embed_query(
        self,
        query: str,
    ):

        return self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):

        query_embedding = self.embed_query(
            query
        )

        return self.vector_store.search(
            query_embedding,
            top_k
        )

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
    ):

        results = self.retrieve(
            query,
            top_k
        )

        context = "\n\n".join(
            f"[{item['section']}]\n{item['text']}"
            for item in results
        )

        return {
            "query": query,
            "context": context,
            "results": results,
        }