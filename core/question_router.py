"""
core/question_router.py

Routes user questions to the appropriate answering engine.

Routing Strategy
----------------
1. Metadata     -> FinancialReport metadata/account
2. Analytics    -> Analytics JSON
3. RAG          -> Vector Search + LLM
"""

from __future__ import annotations

from enum import Enum


class QueryType(str, Enum):
    METADATA = "metadata"
    ANALYTICS = "analytics"
    RAG = "rag"


class QuestionRouter:
    """
    Determines which subsystem should answer a question.
    """

    REASONING_KEYWORDS = {
    "why",
    "explain",
    "reason",
    "how",
    "how can",
    "how do",
    "suggest",
    "recommend",
    "advice",
    "improve",
    "reduce",
    "increase",
    "optimize",
    "analyse",
    "analyze",
    "insight",
    "pattern",
    "patterns",
    "summary",
    "summarize",
}

    METADATA_KEYWORDS = {
        "bank",
        "bank name",
        "statement",
        "statement type",
        "statement period",
        "credit card",
        "debit card",
        "account",
        "account number",
        "account holder",
        "holder",
        "customer id",
        "ifsc",
        "branch",
        "currency",
        "opening balance",
        "closing balance",
    }

    ANALYTICS_KEYWORDS = {
        "expense",
        "expenses",
        "income",
        "spent",
        "spending",
        "cashflow",
        "cash flow",
        "saving",
        "savings",
        "health",
        "score",
        "risk",
        "risks",
        "recommendation",
        "recommendations",
        "merchant",
        "category",
        "categories",
        "highest",
        "lowest",
        "largest",
        "smallest",
        "average",
        "monthly",
        "weekly",
        "daily",
        "transaction count",
        "top spending",
        "behaviour",
        "behavior",
        "kpi",
        "total",
        "count",
        "maximum",
        "minimum",
        "sum",
        "average",
        "highest",
        "lowest",
        "most",
        "least"
    }

    @classmethod
    def classify(cls, question: str) -> QueryType:
        """
        Returns:
            QueryType.METADATA
            QueryType.ANALYTICS
            QueryType.RAG
        """

        q = question.lower().strip()

        # Metadata questions
        for keyword in cls.METADATA_KEYWORDS:
            if keyword in q:
                return QueryType.METADATA

        for keyword in cls.REASONING_KEYWORDS:
            if keyword in q:
                return QueryType.RAG

        # Analytics questions
        for keyword in cls.ANALYTICS_KEYWORDS:
            if keyword in q:
                return QueryType.ANALYTICS

        # Everything else
        return QueryType.RAG