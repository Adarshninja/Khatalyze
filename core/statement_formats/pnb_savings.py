
from __future__ import annotations

import re
from datetime import datetime

from core.statement_formats.base import BaseStatementParser
from models.account import Account
from models.enums import BankName


class PNBSavingsParser(BaseStatementParser):

    @classmethod
    def matches(cls, text: str) -> bool:
        text = text.upper()
        return (
            "PUNJAB NATIONAL BANK" in text
            or "PUNJAB NATIONAL BANK LOGO" in text
            or "PUNB" in text
        )

    def parse(self):
        self.extract_account()
        self.extract_transactions()
        return self.report

    def extract_account(self):
        account = Account()
        account.bank = BankName.PNB

        m = re.search(r"Account No:\s*([0-9]+)", self.text)
        if m:
            account.account_number = m.group(1)

        m = re.search(r"Account No:.*?\n\n([A-Z ]+)\n", self.text, re.S)
        if m:
            account.account_holder = m.group(1).strip()

        m = re.search(r"IFSC Code:\s*([A-Z0-9]+)", self.text)
        if m:
            account.ifsc = m.group(1)

        m = re.search(r"Statement Period:\s*([0-9\-]+)\s*to\s*([0-9\-]+)", self.text)
        if m:
            account.statement_start = datetime.strptime(m.group(1), "%d-%m-%Y")
            account.statement_end = datetime.strptime(m.group(2), "%d-%m-%Y")

        self.report.account = account

    def extract_transactions(self):
        pattern = re.compile(
            r"<tr>\s*"
            r"<td>(?P<date>\d{2}-\d{2}-\d{4})</td>\s*"
            r"<td>₹?(?P<amount>[\d,]+\.\d+)</td>\s*"
            r"<td>(?P<type>DEBIT|CREDIT)</td>\s*"
            r"<td>(?P<instrument>.*?)</td>\s*"
            r"<td>₹?(?P<balance>[\d,]+\.\d+)</td>\s*"
            r"<td>(?P<remarks>.*?)</td>",
            re.S | re.I,
        )

        for m in pattern.finditer(self.text):
            remarks = re.sub(r"<br\s*/?>", " ", m.group("remarks"))
            remarks = re.sub(r"<.*?>", "", remarks)
            remarks = re.sub(r"\s+", " ", remarks).strip()

            raw = {
                "date": m.group("date"),
                "amount": m.group("amount").replace(",", ""),
                "type": m.group("type").upper(),
                "balance": m.group("balance").replace(",", ""),
                "description": remarks,
                "remarks": remarks,
                "reference": m.group("instrument"),
            }

            self.add_transaction(raw)
