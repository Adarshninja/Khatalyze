
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from core.transaction_normalizer import TransactionNormalizer


class StatementParser:
    """
    Parses LlamaParse HTML/Markdown bank statements into a structured format.
    Current implementation is tuned for the SBI layout but is written to be
    easy to extend for additional banks.
    """

    def __init__(self, markdown_file):
        self.markdown_file = Path(markdown_file)

        with open(self.markdown_file, "r", encoding="utf-8") as f:
            self.text = f.read()

        self.data = {
            "bank": None,
            "statement_period": None,
            "account": {},
            "transactions": []
        }

    def extract_bank(self):
        t = self.text.upper()
        if "SBI" in t:
            self.data["bank"] = "SBI"
        elif "AXIS" in t:
            self.data["bank"] = "Axis"
        elif "HDFC" in t:
            self.data["bank"] = "HDFC"
        elif "ICICI" in t:
            self.data["bank"] = "ICICI"
        else:
            self.data["bank"] = "Unknown"

    def extract_statement_period(self):
        m = re.search(r"As on (\d{2}-\d{2}-\d{2})", self.text)
        if m:
            self.data["statement_period"] = m.group(1)

    def _extract_field(self, label):
        m = re.search(
            rf"{re.escape(label)}</td>\s*<td>(.*?)</td>",
            self.text,
            flags=re.DOTALL | re.IGNORECASE
        )
        return m.group(1).strip() if m else None

    def extract_account(self):
        self.data["account"] = {
            "holder": self._extract_field("Name of the Account Holder"),
            "branch": self._extract_field("Branch Name"),
            "ifsc": self._extract_field("IFSC Code"),
            "mode_of_operation": self._extract_field("Mode of Operation")
        }

    def extract_balances(self):
        opening = re.search(r"Opening Balance.*?₹\s*([\d,]+\.\d+)", self.text, re.DOTALL)
        closing = re.search(r"Closing Balance.*?₹\s*([\d,]+\.\d+)", self.text, re.DOTALL)

        if opening:
            self.data["account"]["opening_balance"] = float(opening.group(1).replace(",", ""))
        if closing:
            self.data["account"]["closing_balance"] = float(closing.group(1).replace(",", ""))

    @staticmethod
    def _parse_reference(reference):
        mode = "OTHER"
        ref_no = ""
        party = ""
        bank = ""

        if "/" in reference:
            parts = [p.strip() for p in reference.split("/")]

            if len(parts) > 0:
                mode = parts[0]

            if len(parts) > 2:
                ref_no = parts[2]

            if len(parts) > 3:
                party = parts[3]

            if len(parts) > 4:
                bank = parts[4]

        else:
            party = reference

        return mode, ref_no, party, bank

    def extract_transactions(self):
        soup = BeautifulSoup(self.text, "html.parser")

        for table in soup.find_all("table"):

            headers = [h.get_text(" ", strip=True) for h in table.find_all("th")]

            if "Date" not in headers or "Balance" not in headers:
                continue

            for row in table.find_all("tr"):

                cells = row.find_all("td")

                if len(cells) != 6:
                    continue

                values = [c.get_text(" ", strip=True) for c in cells]

                if "Opening Balance" in values[0]:
                    continue

                if "Closing Balance" in values[0]:
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

                mode, ref_no, party, bank = self._parse_reference(reference)

                raw = {
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

                transaction = TransactionNormalizer.normalize(raw)
                self.data["transactions"].append(transaction)

    def parse(self):
        self.extract_bank()
        self.extract_statement_period()
        self.extract_account()
        self.extract_balances()
        self.extract_transactions()
        return self.data

    def save(self, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

