"""
models/report.py

Master FinancialReport model for FinSight AI.

This object represents an entire bank statement after processing.
Every engine (Analytics, Insights, Risk, Recommendation, RAG)
works on this object.

Architecture:

PDF
 ↓
Parser
 ↓
FinancialReport
 ↓
Analytics
 ↓
Insights
 ↓
Risk
 ↓
Recommendation
 ↓
Dashboard / API / RAG
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from models.account import Account
from models.transaction import Transaction


@dataclass(slots=True)
class FinancialReport:
    """
    Master domain object for FinSight AI.
    """

    # ==========================================================
    # Report Metadata
    # ==========================================================

    report_id: str = ""

    created_at: datetime = field(default_factory=datetime.utcnow)

    version: str = "2.0"

    # ==========================================================
    # Account
    # ==========================================================

    account: Account = field(default_factory=Account)

    # ==========================================================
    # Transactions
    # ==========================================================

    transactions: list[Transaction] = field(default_factory=list)

    # ==========================================================
    # Analytics
    # ==========================================================

    kpis: dict[str, Any] = field(default_factory=dict)

    category_analysis: dict[str, Any] = field(default_factory=dict)

    merchant_statistics: dict[str, Any] = field(default_factory=dict)

    cashflow_analysis: dict[str, Any] = field(default_factory=dict)

    monthly_summary: dict[str, Any] = field(default_factory=dict)

    behavioural_insights: dict[str, Any] = field(default_factory=dict)

    recurring_transactions: list[dict] = field(default_factory=list)

    anomaly_detection: dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Intelligence Layer
    # ==========================================================

    insights: list[str] = field(default_factory=list)

    risks: list[dict] = field(default_factory=list)

    recommendations: list[dict] = field(default_factory=list)

    financial_health_score: float = 0.0

    financial_health_status: str = ""

    # ==========================================================
    # AI Layer
    # ==========================================================

    embeddings_generated: bool = False

    vector_ids: list[str] = field(default_factory=list)

    # ==========================================================
    # Metadata
    # ==========================================================

    metadata: dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Transaction Helpers
    # ==========================================================

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    @property
    def total_transactions(self) -> int:
        return len(self.transactions)

    @property
    def total_income(self) -> float:
        return sum(
            txn.amount
            for txn in self.transactions
            if txn.is_credit
        )

    @property
    def total_expense(self) -> float:
        return sum(
            txn.amount
            for txn in self.transactions
            if txn.is_debit
        )

    @property
    def net_cash_flow(self) -> float:
        return self.total_income - self.total_expense

    # ==========================================================
    # Analytics Helpers
    # ==========================================================

    def update_kpi(self, key: str, value: Any):
        self.kpis[key] = value

    def add_insight(self, insight: str):
        self.insights.append(insight)

    def add_risk(self, risk: dict):
        self.risks.append(risk)

    def add_recommendation(self, recommendation: dict):
        self.recommendations.append(recommendation)

    # ==========================================================
    # Serialization
    # ==========================================================

    def to_dict(self):

        return {
            "report_id": self.report_id,
            "created_at": self.created_at.isoformat(),
            "version": self.version,

            "account": self.account.to_dict(),

            "transactions": [
                t.to_dict()
                for t in self.transactions
            ],

            "kpis": self.kpis,

            "category_analysis": self.category_analysis,

            "merchant_statistics": self.merchant_statistics,

            "cashflow_analysis": self.cashflow_analysis,

            "monthly_summary": self.monthly_summary,

            "behavioural_insights": self.behavioural_insights,

            "recurring_transactions": self.recurring_transactions,

            "anomaly_detection": self.anomaly_detection,

            "insights": self.insights,

            "risks": self.risks,

            "recommendations": self.recommendations,

            "financial_health_score": self.financial_health_score,

            "financial_health_status": self.financial_health_status,

            "embeddings_generated": self.embeddings_generated,

            "vector_ids": self.vector_ids,

            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict):

        report = cls()

        report.report_id = data.get("report_id", "")

        if data.get("created_at"):
            report.created_at = datetime.fromisoformat(
                data["created_at"]
            )

        report.version = data.get("version", "2.0")

        report.account = Account.from_dict(
            data.get("account", {})
        )

        report.transactions = [
            Transaction.from_dict(txn)
            for txn in data.get("transactions", [])
        ]

        report.kpis = data.get("kpis", {})

        report.category_analysis = data.get(
            "category_analysis",
            {}
        )

        report.merchant_statistics = data.get(
            "merchant_statistics",
            {}
        )

        report.cashflow_analysis = data.get(
            "cashflow_analysis",
            {}
        )

        report.monthly_summary = data.get(
            "monthly_summary",
            {}
        )

        report.behavioural_insights = data.get(
            "behavioural_insights",
            {}
        )

        report.recurring_transactions = data.get(
            "recurring_transactions",
            []
        )

        report.anomaly_detection = data.get(
            "anomaly_detection",
            {}
        )

        report.insights = data.get(
            "insights",
            []
        )

        report.risks = data.get(
            "risks",
            []
        )

        report.recommendations = data.get(
            "recommendations",
            []
        )

        report.financial_health_score = data.get(
            "financial_health_score",
            0.0
        )

        report.financial_health_status = data.get(
            "financial_health_status",
            ""
        )

        report.embeddings_generated = data.get(
            "embeddings_generated",
            False
        )

        report.vector_ids = data.get(
            "vector_ids",
            []
        )

        report.metadata = data.get(
            "metadata",
            {}
        )

        return report

    # ==========================================================
    # Pretty Print
    # ==========================================================

    def __str__(self):

        return (
            f"FinancialReport("
            f"{self.account.bank.value}, "
            f"{self.total_transactions} transactions)"
        )

    def __repr__(self):

        return (
            f"FinancialReport("
            f"transactions={self.total_transactions}, "
            f"income={self.total_income}, "
            f"expense={self.total_expense})"
        )
        

