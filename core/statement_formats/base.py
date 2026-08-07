"""
Base parser for all bank statement formats.

Every parser should inherit from this class and only implement
bank-specific extraction logic.
"""

from __future__ import annotations

import re
from pathlib import Path
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from models.report import FinancialReport
from models.enums import BankName
from core.transaction_normalizer import TransactionNormalizer


class BaseStatementParser(ABC):
    """
    Base class for all statement parsers.
    """

    def __init__(self, markdown_file):
        self.markdown_file = Path(markdown_file)

        with open(self.markdown_file, "r", encoding="utf-8") as f:
            self.text = f.read()

        self.soup = BeautifulSoup(self.text, "html.parser")
        self.report = FinancialReport()

    # ---------------------------------------------------------
    # Detection
    # ---------------------------------------------------------

    @classmethod
    @abstractmethod
    def matches(cls, text: str) -> bool:
        """
        Returns True if this parser can parse the statement.
        """
        pass

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def extract_field(self, label: str):
        match = re.search(
            rf"{re.escape(label)}</td>\s*<td>(.*?)</td>",
            self.text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        return None

    def parse_reference(self, reference: str):
        """
        Parse UPI/NEFT/IMPS style references.
        """

        mode = "OTHER"
        reference_number = ""
        party = ""
        bank = ""

        if "/" in reference:

            parts = [x.strip() for x in reference.split("/")]

            if len(parts) > 0:
                mode = parts[0]

            if len(parts) > 2:
                reference_number = parts[2]

            if len(parts) > 3:
                party = parts[3]

            if len(parts) > 4:
                bank = parts[4]

        else:
            party = reference

        return mode, reference_number, party, bank

    def add_transaction(self, raw_transaction: dict):
        txn = TransactionNormalizer.normalize(raw_transaction)
        self.report.add_transaction(txn)

    # ---------------------------------------------------------
    # Common extractors
    # ---------------------------------------------------------

    def extract_bank(self):

        t = self.text.upper()

        if "STATE BANK OF INDIA" in t or "SBI" in t:
            self.report.account.bank = BankName.SBI

        elif "AXIS BANK" in t or "AXIS" in t:
            self.report.account.bank = BankName.AXIS

        elif "HDFC" in t:
            self.report.account.bank = BankName.HDFC

        elif "ICICI" in t:
            self.report.account.bank = BankName.ICICI

        else:
            self.report.metadata["bank"] = "Unknown"

    def extract_statement_period(self):
        pass

    def extract_account(self):
        pass

    def extract_balances(self):
        pass

    # ---------------------------------------------------------
    # Parser
    # ---------------------------------------------------------

    @abstractmethod
    def extract_transactions(self):
        """
        Implemented by child parser.
        """
        pass

    def parse(self):

        self.extract_bank()
        self.extract_statement_period()
        self.extract_account()
        self.extract_balances()
        self.extract_transactions()

        return self.report
    
    