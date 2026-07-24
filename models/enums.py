"""
models/enums.py

Shared enumerations used across the FinSight AI platform.

Using enums instead of raw strings provides:
- Type safety
- IDE autocomplete
- Cleaner validation
- Consistent values across all modules
"""

from enum import Enum


class TransactionType(str, Enum):
    """Type of financial transaction."""

    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class PaymentMode(str, Enum):
    """Transaction payment channel."""

    UPI = "UPI"
    IMPS = "IMPS"
    NEFT = "NEFT"
    RTGS = "RTGS"

    ATM = "ATM"

    CARD = "CARD"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"

    CHEQUE = "CHEQUE"
    CASH = "CASH"

    NET_BANKING = "NET_BANKING"

    WALLET = "WALLET"

    AUTO_DEBIT = "AUTO_DEBIT"

    POS = "POS"

    QR = "QR"

    TRANSFER = "TRANSFER"

    INVESTMENT = "INVESTMENT"

    INTEREST = "INTEREST"

    SALARY = "SALARY"

    OTHER = "OTHER"


class TransactionCategory(str, Enum):
    """
    Normalized spending categories.

    The TransactionNormalizer should map every
    transaction into one of these categories.
    """

    FOOD = "Food"

    SHOPPING = "Shopping"

    GROCERIES = "Groceries"

    TRANSPORT = "Transport"

    FUEL = "Fuel"

    UTILITIES = "Utilities"

    ENTERTAINMENT = "Entertainment"

    HEALTHCARE = "Healthcare"

    EDUCATION = "Education"

    INVESTMENT = "Investment"

    TRANSFER = "Transfer"

    CASH_WITHDRAWAL = "Cash Withdrawal"

    WALLET = "Wallet"

    MERCHANT_PAYMENT = "Merchant Payment"

    UPI = "UPI"

    EMI = "EMI"

    LOAN = "Loan"

    INSURANCE = "Insurance"

    SUBSCRIPTION = "Subscription"

    INTEREST = "Interest"

    TAX = "Tax"

    SALARY = "Salary"

    REFUND = "Refund"

    OTHER = "Other"


class BankName(str, Enum):
    """Supported banks."""

    SBI = "SBI"

    HDFC = "HDFC"

    ICICI = "ICICI"

    AXIS = "Axis"

    KOTAK = "Kotak"

    PNB = "PNB"

    CANARA = "Canara"

    UNION = "Union Bank"

    IDFC = "IDFC First"

    INDUSIND = "IndusInd"

    YES = "Yes Bank"

    UNKNOWN = "Unknown"


class Currency(str, Enum):
    """Supported currencies."""

    INR = "INR"

    USD = "USD"

    EUR = "EUR"

    GBP = "GBP"


class RiskSeverity(str, Enum):
    """Severity of detected financial risk."""

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


class RecommendationPriority(str, Enum):
    """Priority assigned to recommendations."""

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"


class FinancialHealthStatus(str, Enum):
    """
    Overall financial health.

    Derived from Financial Health Score.
    """

    EXCELLENT = "Excellent"

    GOOD = "Good"

    FAIR = "Fair"

    POOR = "Poor"

    CRITICAL = "Critical"


class StatementStatus(str, Enum):
    """Processing lifecycle of a statement."""

    UPLOADED = "UPLOADED"

    PARSED = "PARSED"

    NORMALIZED = "NORMALIZED"

    ANALYZED = "ANALYZED"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"
    
    
    
    
    
    
    
    
    