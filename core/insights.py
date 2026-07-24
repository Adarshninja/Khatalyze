"""
insights.py

Compatibility Insight Engine for FinSight AI.

Supports:
    InsightEngine(analytics_dict)
    InsightEngine(FinancialReport)
"""

from __future__ import annotations

from typing import Any

from models.report import FinancialReport


class InsightEngine:

    def __init__(self, source: dict[str, Any] | FinancialReport):

        self.report_obj = None

        if isinstance(source, FinancialReport):
            self.report_obj = source
            self.report = {
                "kpis": source.kpis,
                "category_analysis": source.category_analysis,
                "merchant_statistics": source.merchant_statistics,
                "behavioural_insights": source.behavioural_insights,
                "monthly_summary": source.monthly_summary,
                "risk_flags": source.metadata.get("risk_flags", []),
                "largest_debit": source.metadata.get("largest_debit", {}),
            }
        else:
            self.report = source

        self.kpis = self.report.get("kpis", {})
        self.categories = self.report.get("category_analysis", {}).get("spending", {})
        self.merchants = self.report.get("merchant_statistics", {})
        self.behaviour = self.report.get("behavioural_insights", {})
        self.monthly = self.report.get("monthly_summary", {})
        self.risks = self.report.get("risk_flags", [])

    def spending_insights(self):
        insights = []
        income = self.kpis.get("income", 0)
        expense = self.kpis.get("expense", 0)
        avg = self.kpis.get("average_debit", 0)
        largest = self.report.get("largest_debit", {})

        if expense:
            insights.append(f"You spent ₹{expense:,.2f} during the statement period.")

        if income:
            savings = income - expense
            rate = (savings / income) * 100 if income else 0
            insights.append(f"You saved ₹{savings:,.2f} ({rate:.1f}% of your income).")

        if avg:
            insights.append(f"Average debit transaction was ₹{avg:,.2f}.")

        if largest:
            amount = largest.get("amount", 0)
            party = largest.get("party", largest.get("description", "Unknown"))
            pct = (amount / expense * 100) if expense else 0
            insights.append(
                f"Largest expense was ₹{amount:,.2f} to {party}, accounting for {pct:.1f}% of total spending."
            )
        return insights

    def category_insights(self):
        insights = []
        if not self.categories:
            return insights
        total = sum(self.categories.values())
        top = max(self.categories, key=self.categories.get)
        insights.append(f"Highest spending category is '{top}'.")
        for cat, value in sorted(self.categories.items(), key=lambda x: x[1], reverse=True):
            pct = value / total * 100 if total else 0
            insights.append(f"{cat} contributed ₹{value:,.2f} ({pct:.1f}%) of total expenses.")
        return insights

    def merchant_insights(self):
        insights = []
        if not self.merchants:
            return insights
        ranked = sorted(self.merchants.items(), key=lambda x: x[1]["total_spent"], reverse=True)
        name, top = ranked[0]
        insights.append(
            f"Most spending was with {name} (₹{top['total_spent']:,.2f} across {top['transaction_count']} transactions)."
        )
        for name, data in ranked[:5]:
            insights.append(
                f"{name}: {data['transaction_count']} transactions, average ₹{data['average_transaction']:,.2f}."
            )
        return insights

    def cashflow_insights(self):
        insights = []
        income = self.kpis.get("income", 0)
        expense = self.kpis.get("expense", 0)
        net = self.kpis.get("net_cash_flow", 0)

        if net > 0:
            insights.append(f"Positive cash flow of ₹{net:,.2f}.")
        elif net < 0:
            insights.append(f"Negative cash flow of ₹{abs(net):,.2f}.")
        else:
            insights.append("Income and expenses are equal.")

        if income:
            insights.append(f"Expenses are {(expense/income)*100:.1f}% of income.")

        return insights

    def behaviour_insights(self):
        insights = []
        if not self.behaviour:
            return insights
        if self.behaviour.get("highest_spending_day"):
            insights.append(f"Highest spending usually occurs on {self.behaviour['highest_spending_day']}.")
        if self.behaviour.get("most_used_category"):
            insights.append(f"Most frequently used category is {self.behaviour['most_used_category']}.")
        if self.behaviour.get("average_daily_spending"):
            insights.append(f"Average daily spending is ₹{self.behaviour['average_daily_spending']:,.2f}.")
        return insights

    def monthly_insights(self):
        insights = []
        for month in sorted(self.monthly.keys()):
            d = self.monthly[month]
            insights.append(
                f"{month}: Income ₹{d['income']:,.2f}, Expense ₹{d['expense']:,.2f}, Savings ₹{d['savings']:,.2f}."
            )
        return insights

    def risk_insights(self):
        return self.risks if self.risks else ["No immediate financial risk flags detected."]

    def generate_report(self):

        insights = {
            "spending_insights": self.spending_insights(),
            "category_insights": self.category_insights(),
            "merchant_insights": self.merchant_insights(),
            "cashflow_insights": self.cashflow_insights(),
            "behaviour_insights": self.behaviour_insights(),
            "monthly_insights": self.monthly_insights(),
            "risk_insights": self.risk_insights(),
        }

        if self.report_obj is None:
            return insights

        self.report_obj.insights = insights
        return self.report_obj
