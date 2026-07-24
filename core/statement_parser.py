import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from core.transaction_normalizer import TransactionNormalizer

class StatementParser:

    def __init__(self, markdown_file):

        self.markdown_file = Path(markdown_file)

        with open(markdown_file, "r", encoding="utf-8") as f:
            self.text = f.read()

        self.data = {
            "bank": None,
            "statement_period": None,
            "account": {},
            "transactions": []
        }

    def extract_bank(self):

        if "SBI" in self.text:
            self.data["bank"] = "SBI"

        elif "AXIS" in self.text.upper():
            self.data["bank"] = "Axis"

        else:
            self.data["bank"] = "Unknown"

    def extract_statement_period(self):

        match = re.search(
            r"As on (\d{2}-\d{2}-\d{2})",
            self.text
        )

        if match:
            self.data["statement_period"] = match.group(1)

    def extract_account_holder(self):

        match = re.search(
            r"Name of the Account Holder</td>\s*<td>(.*?)</td>",
            self.text,
            re.DOTALL
        )

        if match:
            self.data["account"]["holder"] = match.group(1).strip()

    def extract_branch(self):

        match = re.search(
            r"Branch Name</td>\s*<td>(.*?)</td>",
            self.text,
            re.DOTALL
        )

        if match:
            self.data["account"]["branch"] = match.group(1).strip()

    def extract_ifsc(self):

        match = re.search(
            r"IFSC Code</td>\s*<td>(.*?)</td>",
            self.text,
            re.DOTALL
        )

        if match:
            self.data["account"]["ifsc"] = match.group(1).strip()

    def extract_balances(self):

        opening = re.search(
            r"Opening Balance.*?([\d,]+\.\d+)",
            self.text,
            re.DOTALL
        )

        closing = re.search(
            r"Closing Balance.*?([\d,]+\.\d+)",
            self.text,
            re.DOTALL
        )

        if opening:
            self.data["account"]["opening_balance"] = float(
                opening.group(1).replace(",", "")
            )

        if closing:
            self.data["account"]["closing_balance"] = float(
                closing.group(1).replace(",", "")
            )

    def extract_transactions(self):

        soup = BeautifulSoup(self.text, "html.parser")

        tables = soup.find_all("table")

        for table in tables:

            headers = [
                th.get_text(strip=True)
                for th in table.find_all("th")
            ]

            if "Date" not in headers or "Balance" not in headers:
                continue

            rows = table.find_all("tr")

            for row in rows:

                cells = row.find_all("td")

                if len(cells) != 6:
                    continue

                values = [
                    cell.get_text(" ", strip=True)
                    for cell in cells
                ]

                
                if "Opening Balance" in values[0]:
                    continue

                if "Closing Balance" in values[0]:
                    continue

                date = values[0]
                reference = values[1]
                cheque = values[2]
                credit = values[3]
                debit = values[4]
                balance = values[5]

                if credit != "0":
                    txn_type = "CREDIT"
                    amount = float(credit.replace(",", ""))

                else:
                    txn_type = "DEBIT"
                    amount = float(debit.replace(",", ""))


                mode = ""

                if "/" in reference:

                    parts = reference.split("/")

                    if len(parts) > 0:
                        mode = parts[0]

                    ref_no = ""

                    if len(parts) > 2:
                        ref_no = parts[2]

                    party = ""

                    if len(parts) > 3:
                        party = parts[3].strip()

                else:

                    mode = "OTHER"
                    ref_no = ""
                    party = reference

            raw_transaction = {

                "date": date,

                "description": reference,

                "type": txn_type,

                "amount": amount,

                "balance": float(balance.replace(",", "")),

                "cheque_number": cheque
}

        transaction = TransactionNormalizer.normalize(raw_transaction)

        self.data["transactions"].append(transaction)


    def parse(self):

        self.extract_bank()

        self.extract_statement_period()

        self.extract_account_holder()

        self.extract_branch()

        self.extract_ifsc()

        self.extract_balances()

        self.extract_transactions()

        return self.data


    def save(self, output_path):

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output_path, "w", encoding="utf-8") as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )