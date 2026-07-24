
from __future__ import annotations
from typing import Any


class RiskEngine:
    """
    Detects financial risks from the AnalyticsEngine report.

    Output format:
    {
        "financial_health_score": 82,
        "risk_count": 2,
        "risks": [
            {
                "risk_id":"R001",
                "severity":"HIGH",
                "title":"Overspending",
                "description":"Expenses exceeded income by ₹703.00.",
                "recommendation":"Reduce discretionary spending."
            }
        ]
    }
    """

    def __init__(self, analytics_report: dict[str, Any]):
        self.report = analytics_report
        self.kpis = analytics_report.get("kpis", {})
        self.categories = analytics_report.get("category_analysis", {}).get("spending", {})
        self.merchants = analytics_report.get("merchant_statistics", {})
        self.recurring = analytics_report.get("recurring_transactions", {})
        self.behaviour = analytics_report.get("behavioural_insights", {})
        self._risks = []

    def _add(self, rid, severity, title, description, recommendation):
        self._risks.append({
            "risk_id": rid,
            "severity": severity,
            "title": title,
            "description": description,
            "recommendation": recommendation
        })

    def check_negative_cashflow(self):
        income = self.kpis.get("income", 0)
        expense = self.kpis.get("expense", 0)

        if income > 0 and expense > income:
            self._add(
                "R001",
                "HIGH",
                "Overspending",
                f"Expenses exceeded income by ₹{expense-income:,.2f}.",
                "Reduce discretionary spending or increase monthly savings."
            )

    def check_large_transaction(self):
        largest = self.report.get("largest_debit", {})
        amount = largest.get("amount", 0)
        avg = self.kpis.get("average_debit", 0)

        if avg and amount > avg * 5:
            self._add(
                "R002",
                "MEDIUM",
                "Large Transaction",
                f"Detected an unusually large debit of ₹{amount:,.2f}.",
                "Verify this transaction if it was unexpected."
            )

    def check_single_category_dependency(self):
        if not self.categories:
            return

        total = sum(self.categories.values())
        cat = max(self.categories, key=self.categories.get)
        pct = self.categories[cat] / total * 100 if total else 0

        if pct >= 80:
            self._add(
                "R003",
                "LOW",
                "Category Concentration",
                f"{pct:.1f}% of expenses belong to '{cat}'.",
                "Review whether this spending pattern is intentional."
            )

    def check_single_merchant_dependency(self):
        if not self.merchants:
            return

        total = self.kpis.get("expense", 0)

        merchant, data = max(
            self.merchants.items(),
            key=lambda x: x[1]["total_spent"]
        )

        spent = data["total_spent"]

        if total and spent / total >= 0.5:
            self._add(
                "R004",
                "MEDIUM",
                "Merchant Dependency",
                f"{merchant} accounts for {spent/total*100:.1f}% of total spending.",
                "Confirm this spending is expected."
            )

    def check_recurring_payments(self):
        if not self.recurring:
            return

    # Dictionary format
        if isinstance(self.recurring, dict):
            for merchant, data in self.recurring.items():
                if data.get("count", 0) >= 3:
                    self._add(
                    "R005",
                    "LOW",
                    "Recurring Payments",
                    f"Recurring payments detected for {merchant}.",
                    "Check whether these subscriptions are still required."
                )

    # List format
        elif isinstance(self.recurring, list):
            for item in self.recurring:

                merchant = (
                item.get("party")
                or item.get("merchant")
                or item.get("description", "Unknown")
            )

            count = item.get("count", 0)

            if count >= 3:
                self._add(
                    "R005",
                    "LOW",
                    "Recurring Payments",
                    f"Recurring payments detected for {merchant}.",
                    "Check whether these subscriptions are still required."
                )
                
    def check_low_savings_rate(self):
        income = self.kpis.get("income", 0)
        expense = self.kpis.get("expense", 0)

        if income <= 0:
            return

        rate = ((income - expense) / income) * 100

        if rate < 10:
            self._add(
                "R006",
                "MEDIUM",
                "Low Savings Rate",
                f"Savings rate is only {rate:.1f}%.",
                "Aim for a savings rate above 20% where possible."
            )

    def financial_health_score(self):
        score = 100

        for risk in self._risks:
            if risk["severity"] == "HIGH":
                score -= 20
            elif risk["severity"] == "MEDIUM":
                score -= 10
            else:
                score -= 5

        return max(score, 0)

    def analyze(self):
        self._risks.clear()

        self.check_negative_cashflow()
        self.check_large_transaction()
        self.check_single_category_dependency()
        self.check_single_merchant_dependency()
        self.check_recurring_payments()
        self.check_low_savings_rate()

        return {
            "financial_health_score": self.financial_health_score(),
            "risk_count": len(self._risks),
            "risks": self._risks
        }
