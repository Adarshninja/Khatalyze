# from __future__ import annotations

# import json
# import re
# from pathlib import Path

# from bs4 import BeautifulSoup

# from core.transaction_normalizer import TransactionNormalizer
# from models.report import FinancialReport
# from models.enums import BankName


# class StatementParser:
#     """
#     Parses a bank statement into a FinancialReport.
#     """

#     def __init__(self, markdown_file):
#         self.markdown_file = Path(markdown_file)

#         with open(self.markdown_file, "r", encoding="utf-8") as f:
#             self.text = f.read()

#         self.report = FinancialReport()

#     def extract_bank(self):
#         t = self.text.upper()

#         if "SBI" in t:
#             self.report.account.bank = BankName.SBI
#         elif "AXIS" in t:
#             self.report.account.bank = BankName.AXIS
#         elif "HDFC" in t:
#             self.report.account.bank = BankName.HDFC
#         elif "ICICI" in t:
#             self.report.account.bank = BankName.ICICI
#         else:
#             self.report.metadata["bank"] = "Unknown"

#     def extract_statement_period(self):
#         m = re.search(r"As on (\d{2}-\d{2}-\d{2})", self.text)
#         if m:
#             self.report.metadata["statement_period"] = m.group(1)

#     def _extract_field(self, label):
#         m = re.search(
#             rf"{re.escape(label)}</td>\s*<td>(.*?)</td>",
#             self.text,
#             flags=re.DOTALL | re.IGNORECASE,
#         )
#         return m.group(1).strip() if m else None

#     def extract_account(self):
#         self.report.account.holder = self._extract_field("Name of the Account Holder")
#         self.report.account.branch = self._extract_field("Branch Name")
#         self.report.account.ifsc = self._extract_field("IFSC Code")
#         self.report.metadata["mode_of_operation"] = self._extract_field("Mode of Operation")

#     def extract_balances(self):
#         opening = re.search(r"Opening Balance.*?₹\s*([\d,]+\.\d+)", self.text, re.DOTALL)
#         closing = re.search(r"Closing Balance.*?₹\s*([\d,]+\.\d+)", self.text, re.DOTALL)

#         if opening:
#             self.report.account.opening_balance = float(opening.group(1).replace(",", ""))
#         if closing:
#             self.report.account.closing_balance = float(closing.group(1).replace(",", ""))

#     @staticmethod
#     def _parse_reference(reference):
#         mode, ref_no, party, bank = "OTHER", "", "", ""

#         if "/" in reference:
#             parts = [p.strip() for p in reference.split("/")]
#             if len(parts) > 0:
#                 mode = parts[0]
#             if len(parts) > 2:
#                 ref_no = parts[2]
#             if len(parts) > 3:
#                 party = parts[3]
#             if len(parts) > 4:
#                 bank = parts[4]
#         else:
#             party = reference

#         return mode, ref_no, party, bank

#     def extract_transactions(self):
#         soup = BeautifulSoup(self.text, "html.parser")

#         for table in soup.find_all("table"):
#             headers = [h.get_text(" ", strip=True) for h in table.find_all("th")]

#             if "Date" not in headers or "Balance" not in headers:
#                 continue

#             for row in table.find_all("tr"):
#                 cells = row.find_all("td")

#                 if len(cells) != 6:
#                     continue

#                 values = [c.get_text(" ", strip=True) for c in cells]

#                 if "Opening Balance" in values[0] or "Closing Balance" in values[0]:
#                     continue

#                 date, reference, cheque, credit, debit, balance = values

#                 credit = credit.replace(",", "")
#                 debit = debit.replace(",", "")
#                 balance = balance.replace(",", "")

#                 try:
#                     if float(credit) > 0:
#                         txn_type = "CREDIT"
#                         amount = float(credit)
#                     else:
#                         txn_type = "DEBIT"
#                         amount = float(debit)

#                     balance = float(balance)
#                 except ValueError:
#                     continue

#                 mode, ref_no, party, bank = self._parse_reference(reference)

#                 raw = {
#                     "date": date,
#                     "description": reference,
#                     "type": txn_type,
#                     "amount": amount,
#                     "balance": balance,
#                     "cheque_number": cheque,
#                     "mode": mode,
#                     "reference_number": ref_no,
#                     "party": party,
#                     "bank": bank,
#                 }

#                 transaction = TransactionNormalizer.normalize(raw)
#                 self.report.add_transaction(transaction)

#     def parse(self):
#         self.extract_bank()
#         self.extract_statement_period()
#         self.extract_account()
#         self.extract_balances()
#         self.extract_transactions()
#         return self.report

#     def save(self, output_path):
#         output_path = Path(output_path)
#         output_path.parent.mkdir(parents=True, exist_ok=True)

#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(
#                 self.report.to_dict(),
#                 f,
#                 indent=4,
#                 ensure_ascii=False,
#             )


"""
Public entry point for statement parsing.

This class delegates parsing to the appropriate parser.
"""
from pathlib import Path
import json

from core.statement_formats.detector import StatementDetector


class StatementParser:

    def __init__(self, markdown_file):
        self.markdown_file = markdown_file

    def parse(self):
        parser = StatementDetector(self.markdown_file).detect()
        return parser.parse()

    def save(self, output_path):
        report = self.parse()

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                report.to_dict(),
                f,
                indent=4,
                ensure_ascii=False,
            )

        return output_path