"""
models/account.py

Updated Account model for FinSight AI.
Backward-compatible with the new FinancialReport architecture.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any

from models.enums import BankName, Currency


@dataclass(slots=True)
class Account:
    # Primary fields
    account_holder: str = ""
    account_number: str = ""
    bank: BankName = BankName.UNKNOWN
    branch: str = ""
    ifsc: str = ""
    micr: str = ""
    customer_id: str = ""

    # Statement information
    statement_start: datetime | None = None
    statement_end: datetime | None = None
    statement_generated_on: datetime | None = None

    # Financial information
    opening_balance: float = 0.0
    closing_balance: float = 0.0
    currency: Currency = Currency.INR

    # Misc
    account_type: str = ""
    mode_of_operation: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.opening_balance = float(self.opening_balance)
        self.closing_balance = float(self.closing_balance)

    # ------------------------------------------------------------------
    # Compatibility aliases
    # ------------------------------------------------------------------

    @property
    def holder(self) -> str:
        return self.account_holder

    @holder.setter
    def holder(self, value: str):
        self.account_holder = value

    @property
    def statement_period(self):
        return self.metadata.get("statement_period")

    @statement_period.setter
    def statement_period(self, value):
        self.metadata["statement_period"] = value

    @property
    def balance_change(self) -> float:
        return self.closing_balance - self.opening_balance

    @property
    def statement_duration_days(self) -> int:
        if self.statement_start and self.statement_end:
            return (self.statement_end - self.statement_start).days
        return 0

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def to_dict(self):
        data = asdict(self)

        for key in (
            "statement_start",
            "statement_end",
            "statement_generated_on",
        ):
            if data[key]:
                data[key] = data[key].isoformat()

        data["bank"] = self.bank.value
        data["currency"] = self.currency.value
        return data

    @classmethod
    def from_dict(cls, data: dict):
        data = data.copy()

        for key in (
            "statement_start",
            "statement_end",
            "statement_generated_on",
        ):
            if data.get(key):
                try:
                    data[key] = datetime.fromisoformat(data[key])
                except Exception:
                    pass

        if "bank" in data:
            data["bank"] = BankName(data["bank"])

        if "currency" in data:
            data["currency"] = Currency(data["currency"])

        return cls(**data)

    def __str__(self):
        return f"{self.bank.value} | {self.account_holder} | {self.account_number}"

    def __repr__(self):
        return (
            f"Account(holder='{self.account_holder}', "
            f"bank='{self.bank.value}', "
            f"account='{self.account_number}')"
        )


