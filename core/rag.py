"""
core/rag.py

Retrieval-Augmented Generation pipeline for FinSight AI.
"""

from __future__ import annotations

from typing import Any

from core.embeddings import EmbeddingEngine
from core.retriever import Retriever
from core.vector_store import VectorStore
from core.llm import LLMClient

from models.report import FinancialReport


class FinancialRAG:

    def __init__(
        self,
        report: FinancialReport,
        llm: LLMClient | None = None,
        vector_db_path: str = "data/vector_db",
    ):
        self.report = report
        self.vector_db_path = vector_db_path

        self.llm = llm or LLMClient()

        try:
            self.store = VectorStore.load(vector_db_path)

        except Exception:

            embedding_engine = EmbeddingEngine(report)

            result = embedding_engine.generate_embeddings()

            self.store = VectorStore(
                result["embeddings"].shape[1]
            )

            self.store.add_embeddings(
                result["embeddings"],
                result["chunks"],
            )

            self.store.save(vector_db_path)

        self.retriever = Retriever(self.store)

    def build_prompt(
        self,
        question: str,
        top_k: int = 5,
    ) -> str:

        retrieval = self.retriever.retrieve_context(
            question,
            top_k,
        )

        context = retrieval["context"]

        return f"""
You are FinSight AI, an AI-powered Financial Document Intelligence Assistant.

Your role is to analyze bank statements and answer user questions using ONLY the provided financial context.

====================================================
INSTRUCTIONS
====================================================

1. Use ONLY the information from the financial context.
2. Never invent transactions, balances, or numbers.
3. If the answer cannot be determined, explicitly say:
   "The provided financial data does not contain this information."

4. Always present monetary values in Indian Rupees (₹).

5. Explain what the numbers mean instead of only repeating them.

6. Keep the tone professional, concise, and helpful.

7. Whenever appropriate, use Markdown formatting.

====================================================
RESPONSE STYLE
====================================================

Structure your answer like this:

## Summary
A one or two sentence answer.

## Details
- Important figures
- Categories
- Merchants
- Dates (if applicable)

## Insight
Brief financial interpretation.

## Recommendation
Only provide a recommendation if the financial context supports it.

====================================================
FINANCIAL CONTEXT
====================================================

{context}

====================================================
USER QUESTION
====================================================

{question}

====================================================
ANSWER
====================================================
"""

    def ask(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict[str, Any]:

        prompt = self.build_prompt(
            question,
            top_k,
        )

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "answer": answer,
            "context": self.retriever.retrieve_context(
                question,
                top_k,
            ),
        }

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        return self.retriever.retrieve(
            query,
            top_k,
        )

    def rebuild_index(self):

        embedding_engine = EmbeddingEngine(
            self.report,
        )

        result = embedding_engine.generate_embeddings()

        self.store = VectorStore(
            result["embeddings"].shape[1]
        )

        self.store.add_embeddings(
            result["embeddings"],
            result["chunks"],
        )

        self.store.save(
            self.vector_db_path,
        )

        self.retriever = Retriever(
            self.store,
        )
        
        
        
        
        
        
        