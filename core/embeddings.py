
"""
core/embeddings.py

Enhanced semantic chunk generator for FinSight AI.
"""

from __future__ import annotations

from collections import defaultdict
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
                    lines.append(f"  • {sk}: {sv}")
            else:
                lines.append(f"• {key}: {v}")
        return "\n".join(lines)

    def build_chunks(self):
        r = self.report
        chunks = []

        def add(section: str, text: str):
            text = str(text).strip()
            if text:
                chunks.append({
                    "section": section,
                    "text": text,
                    "length": len(text),
                })

        # Executive Summary
        add("executive_summary", f"""
Executive Financial Summary

Account Holder: {getattr(r.account,'account_holder','')}
Bank: {getattr(r.account,'bank','')}
Account Number: {getattr(r.account,'account_number','')}

Opening Balance: {getattr(r.account,'opening_balance',0)}
Closing Balance: {getattr(r.account,'closing_balance',0)}

Total Income: {r.kpis.get('total_income',0)}
Total Expenses: {r.kpis.get('total_expenses',0)}
Net Cash Flow: {r.kpis.get('net_cash_flow',0)}

Financial Health Score: {getattr(r,'financial_health_score','')}
Financial Status: {getattr(r,'financial_health_status','')}
""")

        add("account", f"""
Account Information

Bank: {getattr(r.account,'bank','')}
Account Holder: {getattr(r.account,'account_holder','')}
Account Number: {getattr(r.account,'account_number','')}
""")

        if r.kpis:
            add("kpis", self._fmt_dict("Financial KPIs", r.kpis))

        largest_credit = r.kpis.get("largest_credit", {})
        largest_debit = r.kpis.get("largest_debit", {})

        if largest_credit or largest_debit:
            add("largest_transactions", f"""
Largest Transactions

Largest Credit
Party: {largest_credit.get("party","")}
Amount: {largest_credit.get("amount","")}
Date: {largest_credit.get("date","")}
Category: {largest_credit.get("category","")}

Largest Debit
Party: {largest_debit.get("party","")}
Amount: {largest_debit.get("amount","")}
Date: {largest_debit.get("date","")}
Category: {largest_debit.get("category","")}
""")

        add("financial_health", f"""
Financial Health

Score: {getattr(r,'financial_health_score','')}
Status: {getattr(r,'financial_health_status','')}

Risks
{chr(10).join('- '+x for x in getattr(r,'risks',[]))}
""")

        if r.category_analysis.get("income"):
            add("income_categories",
                self._fmt_dict("Income by Category", r.category_analysis["income"]))

        if r.category_analysis.get("spending"):
            add("expense_categories",
                self._fmt_dict("Spending by Category", r.category_analysis["spending"]))

        if r.behavioural_insights:
            add("behavioural_insights",
                self._fmt_dict("Behavioural Insights", r.behavioural_insights))

        if r.cashflow_analysis:
            add("cashflow_analysis",
                self._fmt_dict("Cashflow Analysis", r.cashflow_analysis))

        if r.monthly_summary:
            add("monthly_summary",
                self._fmt_dict("Monthly Summary", r.monthly_summary))

        if r.merchant_statistics:
            ranked = sorted(
                r.merchant_statistics.items(),
                key=lambda x: x[1].get("total_spent",0),
                reverse=True
            )
            lines = ["Merchant Ranking"]
            for i,(merchant,info) in enumerate(ranked,1):
                lines.append(
f"""
{i}. {merchant}
Spent: {info.get("total_spent",0)}
Transactions: {info.get("transaction_count",0)}
Average: {info.get("average_transaction",0)}
""")
            add("merchant_ranking","\n".join(lines))

        if r.risks:
            add("risk_summary","Financial Risks\n"+"\n".join(f"• {x}" for x in r.risks))

        if r.recommendations:
            lines=["Recommendations"]
            for rec in r.recommendations:
                lines.append(f"""
Title: {rec.get('title','')}
Reason: {rec.get('reason','')}
""")
            add("recommendations","\n".join(lines))

        # Category-wise transaction chunks
        category_groups=defaultdict(list)
        for t in r.transactions:
            cat=getattr(t,"category","")
            if hasattr(cat,"value"):
                cat=cat.value
            category_groups[str(cat)].append(t)

        for category,txns in category_groups.items():
            lines=[f"{category} Transactions"]
            for t in txns:
                ttype=getattr(t,"transaction_type",getattr(t,"type",""))
                if hasattr(ttype,"value"):
                    ttype=ttype.value
                lines.append(
f"""Date: {t.date}
Party: {t.party}
Amount: {t.amount}
Type: {ttype}
""")
            add(f"{category.lower().replace(' ','_')}_transactions","\n".join(lines))

        # Original batches
        batch_size=10
        for i in range(0,len(r.transactions),batch_size):
            lines=[f"Transactions Batch {i//batch_size+1}"]
            for t in r.transactions[i:i+batch_size]:
                cat=getattr(t,"category","")
                if hasattr(cat,"value"):
                    cat=cat.value
                ttype=getattr(t,"transaction_type",getattr(t,"type",""))
                if hasattr(ttype,"value"):
                    ttype=ttype.value
                lines.append(
f"""Date: {t.date}
Party: {t.party}
Amount: {t.amount}
Category: {cat}
Type: {ttype}
""")
            add(f"transactions_{i//batch_size+1}","\n".join(lines))

        return chunks

    def generate_embeddings(self):
        chunks=self.build_chunks()
        texts=[c["text"] for c in chunks]
        embeddings=self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        self.report.embeddings_generated=True
        return {"chunks":chunks,"embeddings":embeddings}

    @staticmethod
    def embedding_dimension():
        return SentenceTransformer(
            EmbeddingEngine.MODEL_NAME
        ).get_sentence_embedding_dimension()

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray):
        return float(np.dot(v1, v2))

