from __future__ import annotations

import re
from datetime import datetime
from bs4 import BeautifulSoup

from core.statement_formats.base import BaseStatementParser
from models.account import Account
from models.enums import BankName


class AxisCreditCardParser(BaseStatementParser):

    @classmethod
    def matches(cls, text: str) -> bool:
        t = text.upper()
        return (
            "PAYMENT SUMMARY" in t
            and "ACCOUNT SUMMARY" in t
            and "TRANSACTION DETAILS" in t
            and "AMOUNT (RS.)" in t
        )

    def extract_account(self):
        account = Account()

        account.bank = BankName.AXIS

        m = re.search(
            r"Card No:\s*([0-9*]+)\s*Name\s*([A-Z ]+)",
            self.text,
            re.IGNORECASE,
        )

        if m:
            account.account_number = m.group(1).strip()
            account.holder = m.group(2).strip()

        self.report.account = account

    def extract_statement_period(self):
        m = re.search(
            r"Statement Period.*?<td>(.*?)</td>",
            self.text,
            re.IGNORECASE | re.DOTALL,
        )

        if not m:
            return

        period = re.sub("<.*?>", "", m.group(1)).strip()

        if "-" not in period:
            return

        start, end = [x.strip() for x in period.split("-")]

        self.report.metadata["statement_period"] = {
            "from": start,
            "to": end,
        }

    def parse_amount(self, value):

        value = value.replace(",", "").strip()

        if value.endswith("Dr"):
            return "DEBIT", float(value[:-2].strip())

        if value.endswith("Cr"):
            return "CREDIT", float(value[:-2].strip())

        return None, None

    def extract_transactions(self):

        soup = BeautifulSoup(self.text, "html.parser")

        tables = soup.find_all("table")

        for table in tables:

            headers = [
                th.get_text(" ", strip=True).upper()
                for th in table.find_all("th")
            ]

            if "TRANSACTION DETAILS" not in " ".join(headers):
                continue

            for row in table.find_all("tr"):

                cells = row.find_all("td")

                if len(cells) != 4:
                    continue

                date = cells[0].get_text(" ", strip=True)

                if not re.match(r"\d{2}/\d{2}/\d{4}", date):
                    continue

                description = cells[1].get_text(" ", strip=True)

                merchant = cells[2].get_text(" ", strip=True)

                amount_text = cells[3].get_text(" ", strip=True)

                txn_type, amount = self.parse_amount(amount_text)

                if txn_type is None:
                    continue

                raw = {
                    "date": date,
                    "description": description,
                    "amount": amount,
                    "type": txn_type,
                    "balance": 0.0,
                    "reference_number": "",
                    "cheque_number": "",
                    "mode": "CARD",
                    "party": description,
                    "merchant_category": merchant,
                    "bank": "Axis Bank",
                }

                self.add_transaction(raw)

    def parse(self):

        self.extract_account()

        self.extract_statement_period()

        self.extract_transactions()

        self.report.metadata["statement_type"] = "credit_card"

        self.report.metadata["parsed_at"] = datetime.utcnow().isoformat()

        return self.report
