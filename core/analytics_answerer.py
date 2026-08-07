"""
Answers analytics-related questions directly from FinancialReport.

No vector search.
No embeddings.
No LLM.
"""

from __future__ import annotations

from models.report import FinancialReport


class AnalyticsAnswerer:
    

    @staticmethod
    def answer(question: str, report: FinancialReport):
        
        print("=" * 60)
        print(report.kpis)
        print(report.cashflow_analysis)
        print(report.category_analysis)
        print("=" * 60)

        q = question.lower()

        kpis = report.kpis or {}
        categories = report.category_analysis or {}
        merchants = report.merchant_statistics or {}
        cashflow = report.cashflow_analysis or {}
        risks = report.risks or []
        recommendations = report.recommendations or []

        # --------------------------------------------------
        # Income
        # --------------------------------------------------

        if "income" in q:

            value = kpis.get("income")

            if value is not None:
                return f"Total Income: ₹{value:,.2f}"

        # --------------------------------------------------
        # Expense / Spending
        # --------------------------------------------------

        if (
            "expense" in q
            or "spending" in q
            or "spent" in q
        ):

            value = kpis.get("expense")

            if value is not None:
                return f"Total Spending: ₹{value:,.2f}"
            
        # --------------------------------------------------
        # Average Debit
        # --------------------------------------------------

            if "average debit" in q:

                 value = kpis.get("average_debit")

            if value is not None:
                return f"Average Debit: ₹{value:,.2f}"
            
        # --------------------------------------------------
        # Average Credit
        # --------------------------------------------------

            if "average credit" in q:
                value = kpis.get("average_credit")

            if value is not None:
                return f"Average Credit: ₹{value:,.2f}"

        # --------------------------------------------------
        # Savings
        # --------------------------------------------------

        if "saving" in q:

            value = kpis.get("savings")

            if value is not None:
                return f"Total Savings: ₹{value:,.2f}"

        # --------------------------------------------------
        # Savings Rate
        # --------------------------------------------------

        if "saving rate" in q:

            rate = kpis.get("savings_rate")

            if rate is not None:
                return f"Savings Rate: {rate:.2f}%"

        # --------------------------------------------------
        # Total Transactions
        # --------------------------------------------------

        if "transaction" in q and (
            "count" in q
            or "total" in q
            or "how many" in q
        ):

            return f"Total Transactions: {len(report.transactions)}"

        # --------------------------------------------------
        # Highest Expense Category
        # --------------------------------------------------

        if (
            "highest category" in q
            or "largest category" in q
            or "most spending category" in q
            or "top category" in q
        ):

            categories = kpis.get("expense_categories", {})

            if categories:

                category = max(
                    categories,
                    key=categories.get,
                )

                amount = categories[category]

                return (
                    f"Highest spending category is "
                    f"{category} "
                    f"(₹{amount:,.2f})"
                )

        # --------------------------------------------------
        # Financial Score
        # --------------------------------------------------

        if (
            "score" in q
            or "financial health" in q
        ):

            score = report.financial_health_score
            status = report.financial_health_status

            if score is not None:

                return (
                    f"Financial Health Score: {score}/100\n"
                    f"Status: {status}"
                )

        # --------------------------------------------------
        # Risks
        # --------------------------------------------------

        if "risk" in q:

            if not risks:
                return "No financial risks detected."

            text = []

            for risk in risks:

                text.append(
                    f"• [{risk.severity}] {risk.title}"
                )

            return "\n".join(text)

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        if (
            "recommendation" in q
            or "advice" in q
            or "suggestion" in q
        ):

            if not recommendations:
                return "No recommendations available."

            lines = []

            for rec in recommendations:

                lines.append(
                    f"• {rec.title}"
                )

            return "\n".join(lines)

        # --------------------------------------------------
        # Largest Transaction
        # --------------------------------------------------

        if (
            "largest transaction" in q
            or "highest transaction" in q
        ):

            if not report.transactions:
                return "No transactions found."

            txn = max(
                report.transactions,
                key=lambda x: x.amount,
            )

            return (
                f"Largest transaction:\n"
                f"₹{txn.amount:,.2f}\n"
                f"{txn.description}"
            )

        # --------------------------------------------------
        # Merchant
        # --------------------------------------------------

        if (
            "merchant" in q
            and (
                "highest" in q
                or "largest" in q
                or "most" in q
            )
        ):

            merchants = kpis.get(
                "merchant_analysis",
                {},
            )

            if merchants:

                merchant = max(
                    merchants,
                    key=lambda x: merchants[x]["total"],
                )

                total = merchants[merchant]["total"]

                return (
                    f"Highest paid merchant:\n"
                    f"{merchant}\n"
                    f"₹{total:,.2f}"
                )

        return (
             "This analytics question isn't implemented yet. "
    "Please ask another question or extend AnalyticsAnswerer."
        )
    