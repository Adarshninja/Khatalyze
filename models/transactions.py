"""
models/transaction.py

Canonical Transaction model used throughout FinSight AI.

Every bank parser should return Transaction objects instead of
raw dictionaries.

This object is consumed by:

- Analytics Engine
- Insight Engine
- Risk Engine
- Recommendation Engine
- RAG Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any
import uuid

from models.enums import (
    TransactionType,
    PaymentMode,
    TransactionCategory,
    BankName,
    Currency,
)


@dataclass(slots=True)
class Transaction:
    """
    Canonical financial transaction.
    """

    # ------------------------------------------------------------------
    # Core Identity
    # ------------------------------------------------------------------

    transaction_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    # ------------------------------------------------------------------
    # Date
    # ------------------------------------------------------------------

    date: datetime | None = None

    # ------------------------------------------------------------------
    # Transaction Details
    # ------------------------------------------------------------------

    description: str = ""

    party: str = ""

    amount: float = 0.0

    balance: float = 0.0

    transaction_type: TransactionType = TransactionType.DEBIT

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    category: TransactionCategory = TransactionCategory.OTHER

    payment_mode: PaymentMode = PaymentMode.OTHER

    bank: BankName = BankName.UNKNOWN

    currency: Currency = Currency.INR

    # ------------------------------------------------------------------
    # Banking Metadata
    # ------------------------------------------------------------------

    reference_number: str = ""

    cheque_number: str = ""

    branch: str = ""

    remarks: str = ""

    # ------------------------------------------------------------------
    # Intelligence Metadata
    # ------------------------------------------------------------------

    confidence: float = 1.0

    tags: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ============================================================
    # Validation
    # ============================================================

    def __post_init__(self):

        self.amount = float(self.amount)

        self.balance = float(self.balance)

        self.confidence = float(self.confidence)

        if self.amount < 0:
            raise ValueError("Amount cannot be negative.")

        if not (0 <= self.confidence <= 1):
            raise ValueError("Confidence must lie between 0 and 1.")

    # ============================================================
    # Helper Properties
    # ============================================================

    @property
    def is_credit(self) -> bool:
        return self.transaction_type == TransactionType.CREDIT

    @property
    def is_debit(self) -> bool:
        return self.transaction_type == TransactionType.DEBIT

    # ============================================================
    # Tag Helpers
    # ============================================================

    def add_tag(self, tag: str):
        tag = tag.strip()

        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)

    # ============================================================
    # Metadata Helpers
    # ============================================================

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    # ============================================================
    # Serialization
    # ============================================================

    def to_dict(self) -> dict:

        data = asdict(self)

        if self.date:
            data["date"] = self.date.isoformat()

        data["transaction_type"] = self.transaction_type.value
        data["payment_mode"] = self.payment_mode.value
        data["category"] = self.category.value
        data["bank"] = self.bank.value
        data["currency"] = self.currency.value

        return data

    @classmethod
    def from_dict(cls, data: dict):

        data = data.copy()

        if data.get("date"):
            try:
                data["date"] = datetime.fromisoformat(data["date"])
            except Exception:
                pass

        if "transaction_type" in data:
            data["transaction_type"] = TransactionType(
                data["transaction_type"]
            )

        if "payment_mode" in data:
            data["payment_mode"] = PaymentMode(
                data["payment_mode"]
            )

        if "category" in data:
            data["category"] = TransactionCategory(
                data["category"]
            )

        if "bank" in data:
            data["bank"] = BankName(
                data["bank"]
            )

        if "currency" in data:
            data["currency"] = Currency(
                data["currency"]
            )

        return cls(**data)

    # ============================================================
    # Pretty Print
    # ============================================================

    def __str__(self):

        return (
            f"{self.date} | "
            f"{self.transaction_type.value} | "
            f"₹{self.amount:,.2f} | "
            f"{self.party}"
        )

    def __repr__(self):

        return (
            f"Transaction("
            f"id={self.transaction_id}, "
            f"type={self.transaction_type.value}, "
            f"amount={self.amount}, "
            f"party='{self.party}')"
        )
        
        
        
        
        
        