"""
Answers metadata questions directly from FinancialReport.
No vector search.
No LLM.
"""

from __future__ import annotations


class MetadataAnswerer:

    @staticmethod
    def answer(question: str, report):

        q = question.lower()

        # ---------------------------------------------------
        # Statement Type
        # ---------------------------------------------------

        if "credit card" in q or "debit card" in q or "statement type" in q:

            statement_type = report.metadata.get(
                "statement_type",
                "Unknown"
            )

            if statement_type == "credit_card":
                return "This is a Credit Card statement."

            if statement_type == "savings":
                return "This is a Savings Account statement."

            return f"Statement type: {statement_type}"

        # ---------------------------------------------------
        # Bank
        # ---------------------------------------------------

        if "bank" in q:

            if report.account.bank:
                return f"Bank: {report.account.bank.value}"

            return "Bank information is unavailable."

        # ---------------------------------------------------
        # Account Holder
        # ---------------------------------------------------

        if "holder" in q or "account holder" in q:

            if report.account.account_holder:
                return f"Account Holder: {report.account.account_holder}"

            return "Account holder information is unavailable."

        # ---------------------------------------------------
        # Account Number
        # ---------------------------------------------------

        if "account number" in q:

            if report.account.account_number:
                return f"Account Number: {report.account.account_number}"

            return "Account number unavailable."

        # ---------------------------------------------------
        # Statement Period
        # ---------------------------------------------------

        if "statement period" in q or "period" in q:

            period = report.metadata.get("statement_period")

            if period:
                return (
                    f"Statement Period: "
                    f"{period['from']} to {period['to']}"
                )

            return "Statement period unavailable."

        # ---------------------------------------------------
        # Currency
        # ---------------------------------------------------

        if "currency" in q:

            return report.account.currency.value

        return None