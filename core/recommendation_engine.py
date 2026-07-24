
"""
recommendation_engine.py

Compatibility Recommendation Engine for FinSight AI.

Supports:
    RecommendationEngine(FinancialReport)
    RecommendationEngine(dict)
"""

from __future__ import annotations
from typing import Any
from models.report import FinancialReport


class RecommendationEngine:

    def __init__(self, source: dict[str, Any] | FinancialReport):
        self.report_obj = None

        if isinstance(source, FinancialReport):
            self.report_obj = source
            self.report = {
                "kpis": source.kpis,
                "category_analysis": source.category_analysis,
                "merchant_statistics": source.merchant_statistics,
                "risks": source.risks,
                "behavioural_insights": source.behavioural_insights,
                "recurring_transactions": source.recurring_transactions,
            }
        else:
            self.report = source

        self.kpis = self.report.get("kpis", {})
        self.categories = self.report.get("category_analysis", {}).get("spending", {})
        self.merchants = self.report.get("merchant_statistics", {})
        self.risks = self.report.get("risks", [])
        self.behaviour = self.report.get("behavioural_insights", {})
        self.recurring = self.report.get("recurring_transactions", [])

    def _add(self, recs, priority, title, reason, action):
        recs.append({
            "priority": priority,
            "title": title,
            "reason": reason,
            "recommended_action": action,
        })

    def generate_report(self):
        recs = []

        income = float(self.kpis.get("income", 0))
        expense = float(self.kpis.get("expense", 0))

        if income and expense > income:
            self._add(
                recs, "HIGH",
                "Reduce Monthly Spending",
                f"Expenses exceeded income by ₹{expense-income:.2f}.",
                "Create a monthly budget and reduce discretionary spending."
            )

        if income:
            savings_rate = ((income-expense)/income)*100
            if savings_rate < 0:
                self._add(
                    recs, "HIGH",
                    "Increase Savings",
                    f"Savings rate is {savings_rate:.1f}%.",
                    "Aim for a positive monthly savings rate."
                )
            elif savings_rate < 20:
                self._add(
                    recs, "MEDIUM",
                    "Improve Savings Rate",
                    f"Savings rate is {savings_rate:.1f}%.",
                    "Target saving at least 20% of monthly income."
                )

        if self.categories:
            top = max(self.categories, key=self.categories.get)
            total = sum(self.categories.values())
            pct = (self.categories[top] / total) * 100 if total else 0
            if pct >= 70:
                self._add(
                    recs, "MEDIUM",
                    "Diversify Spending",
                    f"{pct:.1f}% of spending is in '{top}'.",
                    "Review whether this concentration is intentional."
                )

        if self.merchants:
            name, data = max(
                self.merchants.items(),
                key=lambda x: x[1]["total_spent"]
            )
            total_spent = sum(v["total_spent"] for v in self.merchants.values())
            pct = (data["total_spent"]/total_spent)*100 if total_spent else 0
            if pct >= 50:
                self._add(
                    recs, "LOW",
                    "Review Major Merchant",
                    f"{name} accounts for {pct:.1f}% of spending.",
                    "Verify recurring or unusually high payments."
                )

        if self.recurring:
            parties = ", ".join(r["party"] for r in self.recurring[:3])
            self._add(
                recs, "LOW",
                "Review Recurring Payments",
                f"Recurring payments detected: {parties}.",
                "Cancel subscriptions that are no longer required."
            )

        if self.risks:
            self._add(
                recs, "MEDIUM",
                "Resolve Financial Risks",
                f"{len(self.risks)} risk(s) detected.",
                "Review the Risk Report and address high-severity issues first."
            )

        if not recs:
            self._add(
                recs, "LOW",
                "Financial Health",
                "No major issues detected.",
                "Continue maintaining your current financial habits."
            )

        if self.report_obj is None:
            return recs

        self.report_obj.recommendations = recs
        return self.report_obj


