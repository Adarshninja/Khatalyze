"""
Automatically detects which parser should be used
for a given statement.
"""

from __future__ import annotations

from core.statement_formats.sbi_savings import SBISavingsParser
from core.statement_formats.axis_credit_card import AxisCreditCardParser
from core.statement_formats.pnb_savings import PNBSavingsParser

class StatementDetector:

    def __init__(self, markdown_file):
        self.markdown_file = markdown_file

        with open(markdown_file, "r", encoding="utf-8") as f:
            self.text = f.read()

    def detect(self):

        # SBI Savings Statement
        if SBISavingsParser.matches(self.text):
            print("Detected: SBI Savings Statement")
            return SBISavingsParser(self.markdown_file)

        # Axis Credit Card Statement
        if AxisCreditCardParser.matches(self.text):
            print("Detected: Axis Credit Card Statement")
            return AxisCreditCardParser(self.markdown_file)
        
        if PNBSavingsParser.matches(self.text):
            print("Detected: PNB Savings Statement")
            return PNBSavingsParser(self.markdown_file)

        raise ValueError(
            "Unsupported statement format.\n"
            "No parser is available for this statement."
        )
        
        