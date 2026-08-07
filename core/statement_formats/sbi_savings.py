from __future__ import annotations

import json
import re

from core.statement_formats.base import BaseStatementParser


class SBISavingsParser(BaseStatementParser):
    """
    Parser for SBI-style savings account statements.
    """

    @classmethod
    def matches(cls, text: str) -> bool:
        text = text.upper()
        return (
            "TRANSACTION REFERENCE" in text
            and "BALANCE" in text
            and ("SBI" in text or "STATE BANK OF INDIA" in text)
        )

    def extract_statement_period(self):
        m = re.search(r"As on (\d{2}-\d{2}-\d{2})", self.text)
        if m:
            self.report.metadata["statement_period"] = m.group(1)

    def extract_account(self):
        self.report.account.holder = self.extract_field("Name of the Account Holder")
        self.report.account.branch = self.extract_field("Branch Name")
        self.report.account.ifsc = self.extract_field("IFSC Code")
        self.report.metadata["mode_of_operation"] = self.extract_field("Mode of Operation")

    def extract_balances(self):
        opening = re.search(r"Opening Balance.*?₹\s*([\d,]+\.\d+)", self.text, re.DOTALL)
        closing = re.search(r"Closing Balance.*?₹\s*([\d,]+\.\d+)", self.text, re.DOTALL)

        if opening:
            self.report.account.opening_balance = float(opening.group(1).replace(",", ""))

        if closing:
            self.report.account.closing_balance = float(closing.group(1).replace(",", ""))

    def extract_transactions(self):
        for table in self.soup.find_all("table"):

            headers = [h.get_text(" ", strip=True).upper() for h in table.find_all("th")]

            if not (
                "DATE" in headers
                and "BALANCE" in headers
                and "CREDIT" in headers
                and "DEBIT" in headers
            ):
                continue

            for row in table.find_all("tr"):

                cells = row.find_all("td")

                if len(cells) != 6:
                    continue

                values = [c.get_text(" ", strip=True) for c in cells]

                if (
                    "OPENING BALANCE" in values[0].upper()
                    or "CLOSING BALANCE" in values[0].upper()
                ):
                    continue

                date, reference, cheque, credit, debit, balance = values

                credit = credit.replace(",", "")
                debit = debit.replace(",", "")
                balance = balance.replace(",", "")

                try:
                    if float(credit) > 0:
                        txn_type = "CREDIT"
                        amount = float(credit)
                    else:
                        txn_type = "DEBIT"
                        amount = float(debit)

                    balance = float(balance)

                except ValueError:
                    continue

                mode, ref_no, party, bank = self.parse_reference(reference)

                self.add_transaction(
                    {
                        "date": date,
                        "description": reference,
                        "type": txn_type,
                        "amount": amount,
                        "balance": balance,
                        "cheque_number": cheque,
                        "mode": mode,
                        "reference_number": ref_no,
                        "party": party,
                        "bank": bank,
                    }
                )

    def save(self, output_path):
        from pathlib import Path

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                self.report.to_dict(),
                f,
                indent=4,
                ensure_ascii=False,
            )

