
"""
core/embeddings.py

Human-readable semantic chunk generator for FinSight AI.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

from models.report import FinancialReport


class EmbeddingEngine:
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self, report: FinancialReport):
        self.report = report
        self.model = SentenceTransformer(self.MODEL_NAME)

    def _fmt_dict(self, title: str, data: dict) -> str:
        lines = [title]
        for k, v in data.items():
            key = str(k).replace("_", " ").title()
            if isinstance(v, dict):
                lines.append(f"\n{key}:")
                for sk, sv in v.items():
                    lines.append(f"  • {sk}: ₹{sv}")
            else:
                lines.append(f"• {key}: {v}")
        return "\n".join(lines)

    def build_chunks(self):
        r = self.report
        chunks = []

        def add(section, text):
            text = text.strip()
            if text:
                chunks.append({"section": section, "text": text})

        add(
            "account",
            f"""
Account Information

Bank: {getattr(r.account,'bank','')}
Account Holder: {getattr(r.account,'account_holder','')}
Account Number: {getattr(r.account,'account_number','')}
""",
        )

        if r.kpis:
            add("kpis", self._fmt_dict("Financial KPIs", r.kpis))

        if r.category_analysis.get("income"):
            add(
                "income_categories",
                self._fmt_dict(
                    "Income by Category",
                    r.category_analysis["income"],
                ),
            )

        if r.category_analysis.get("spending"):
            add(
                "expense_categories",
                self._fmt_dict(
                    "Spending by Category",
                    r.category_analysis["spending"],
                ),
            )

        if r.merchant_statistics:
            lines = ["Merchant Statistics"]
            for merchant, info in r.merchant_statistics.items():
                lines.append(
                    f"""• Merchant: {merchant}
  - Total Spent: ₹{info.get('total_spent', 0):,.2f}
  - Transactions: {info.get('transaction_count', 0)}
  - Average Transaction: ₹{info.get('average_transaction', 0):,.2f}
"""
        )
            add("merchant_statistics", "\n".join(lines))

        if r.behavioural_insights:
            add(
                "behavioural_insights",
                self._fmt_dict(
                    "Behavioural Insights",
                    r.behavioural_insights,
                ),
            )

        if r.cashflow_analysis:
            add(
                "cashflow_analysis",
                "Cashflow Analysis\n"
                + "\n".join(
                    f"• {k.replace('_',' ').title()}: {v}"
                    for k, v in r.cashflow_analysis.items()
                    if not isinstance(v, list)
                ),
            )

        if r.monthly_summary:
            add(
                "monthly_summary",
                self._fmt_dict("Monthly Summary", r.monthly_summary),
            )

        if r.risks:
            add(
                "risks",
                "Financial Risks\n"
                + "\n".join(f"• {risk}" for risk in r.risks),
            )

        if r.recommendations:
            add(
                "recommendations",
                "Recommendations\n"
                + "\n".join(
                    f"• {rec.get('title','')}: {rec.get('reason','')}"
                    for rec in r.recommendations
                ),
            )

        batch_size = 10
        for i in range(0, len(r.transactions), batch_size):
            lines = [f"Transactions Batch {i//batch_size+1}"]
            for t in r.transactions[i:i+batch_size]:
                category = getattr(t, "category", "")
                if hasattr(category, "value"):
                    category = category.value
                ttype = getattr(t, "transaction_type", getattr(t, "type", ""))
                if hasattr(ttype, "value"):
                    ttype = ttype.value
                lines.append(
                    f"""Date: {t.date}
Party: {t.party}
Amount: ₹{t.amount}
Category: {category}
Type: {ttype}
"""
                )
            add(f"transactions_{i//batch_size+1}", "\n".join(lines))

        return chunks

    def generate_embeddings(self):
        chunks = self.build_chunks()
        texts = [c["text"] for c in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        self.report.embeddings_generated = True

        return {
            "chunks": chunks,
            "embeddings": embeddings,
        }

    @staticmethod
    def embedding_dimension():
        return SentenceTransformer(
            EmbeddingEngine.MODEL_NAME
        ).get_sentence_embedding_dimension()

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray):
        return float(np.dot(v1, v2))
