
from __future__ import annotations
from typing import Any


class InsightEngine:
    """
    Converts analytics output into human-readable financial insights.
    """

    def __init__(self, analytics_report: dict[str, Any]):
        self.report = analytics_report
        self.kpis = analytics_report.get("kpis", {})
        self.categories = analytics_report.get("category_analysis", {}).get("spending", {})
        self.merchants = analytics_report.get("merchant_statistics", {})
        self.behaviour = analytics_report.get("behavioural_insights", {})
        self.monthly = analytics_report.get("monthly_summary", {})
        self.risks = analytics_report.get("risk_flags", [])

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
        top_cat = max(self.categories, key=self.categories.get)

        for cat, value in sorted(self.categories.items(), key=lambda x: x[1], reverse=True):
            pct = (value / total * 100) if total else 0
            insights.append(f"{cat} contributed ₹{value:,.2f} ({pct:.1f}%) of total expenses.")

        insights.insert(0, f"Highest spending category is '{top_cat}'.")
        return insights

    def merchant_insights(self):
        insights = []
        if not self.merchants:
            return insights

        sorted_merchants = sorted(
            self.merchants.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )

        top_name, top = sorted_merchants[0]
        insights.append(
            f"Most spending was with {top_name} (₹{top['total_spent']:,.2f} across {top['transaction_count']} transactions)."
        )

        for name, data in sorted_merchants[:5]:
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
            ratio = (expense / income) * 100
            insights.append(f"Expenses are {ratio:.1f}% of income.")

        return insights

    def behaviour_insights(self):
        insights = []
        if not self.behaviour:
            return insights

        if self.behaviour.get("highest_spending_day"):
            insights.append(
                f"Highest spending usually occurs on {self.behaviour['highest_spending_day']}."
            )

        if self.behaviour.get("most_used_category"):
            insights.append(
                f"Most frequently used category is {self.behaviour['most_used_category']}."
            )

        if self.behaviour.get("average_daily_spending"):
            insights.append(
                f"Average daily spending is ₹{self.behaviour['average_daily_spending']:,.2f}."
            )

        return insights

    def monthly_insights(self):
        insights = []

        if not self.monthly:
            return insights

        months = sorted(self.monthly.keys())
        for month in months:
            data = self.monthly[month]
            insights.append(
                f"{month}: Income ₹{data['income']:,.2f}, Expense ₹{data['expense']:,.2f}, Savings ₹{data['savings']:,.2f}."
            )

        return insights

    def risk_insights(self):
        if not self.risks:
            return ["No immediate financial risk flags detected."]
        return self.risks

    def generate_report(self):
        return {
            "spending_insights": self.spending_insights(),
            "category_insights": self.category_insights(),
            "merchant_insights": self.merchant_insights(),
            "cashflow_insights": self.cashflow_insights(),
            "behaviour_insights": self.behaviour_insights(),
            "monthly_insights": self.monthly_insights(),
            "risk_insights": self.risk_insights(),
        }
