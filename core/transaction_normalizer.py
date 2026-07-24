"""
Refactored Transaction Normalizer for FinSight AI.
"""
from __future__ import annotations
import re
from datetime import datetime
from models.transaction import Transaction
from models.enums import TransactionType,TransactionCategory,PaymentMode,BankName,Currency

class TransactionNormalizer:
    @classmethod
    def normalize(cls, txn:dict)->Transaction:
        d=txn.get("description","").strip()
        return Transaction(
            date=cls._parse_date(txn.get("date")),
            description=d,
            party=cls.detect_party(d),
            amount=float(txn.get("amount",0)),
            balance=float(txn.get("balance",0)),
            transaction_type=TransactionType(txn.get("type","DEBIT")),
            payment_mode=cls.detect_mode(d),
            category=cls.detect_category(d),
            bank=cls.detect_bank(d),
            currency=Currency.INR,
            reference_number=cls.detect_reference(d),
            cheque_number=txn.get("cheque_number",""),
        )

    @staticmethod
    def _parse_date(v):
        if not v: return None
        for f in ("%d-%m-%y","%d-%m-%Y","%d/%m/%Y"):
            try: return datetime.strptime(v,f)
            except: pass
        return None

    @staticmethod
    def detect_mode(t):
        u=t.upper()
        if u.startswith("UPI"): return PaymentMode.UPI
        if u.startswith("ATM"): return PaymentMode.ATM
        if u.startswith("NEFT"): return PaymentMode.NEFT
        if u.startswith("IMPS"): return PaymentMode.IMPS
        if u.startswith("RTGS"): return PaymentMode.RTGS
        if "INTEREST CREDIT" in u: return PaymentMode.INTEREST
        if "SALARY" in u: return PaymentMode.SALARY
        return PaymentMode.OTHER

    @staticmethod
    def detect_reference(t):
        m=re.search(r"/(\d{6,})/",t)
        return m.group(1) if m else ""

    @staticmethod
    def detect_party(t):
        p=t.split("/")
        return p[3].strip() if len(p)>=4 else ""

    @staticmethod
    def detect_bank(t):
        u=t.upper()
        mp={"SBIN":BankName.SBI,"PUNB":BankName.PNB,"HDFC":BankName.HDFC,"ICIC":BankName.ICICI,"YESB":BankName.YES,"UTIB":BankName.AXIS,"KKBK":BankName.KOTAK,"INDB":BankName.INDUSIND,"IDFC":BankName.IDFC}
        for k,v in mp.items():
            if k in u: return v
        return BankName.UNKNOWN

    @staticmethod
    def detect_category(t):
        u=t.upper()
        rules=[("GROWW",TransactionCategory.INVESTMENT),("ZERODHA",TransactionCategory.INVESTMENT),("BHARATPE",TransactionCategory.MERCHANT_PAYMENT),("PAYTM",TransactionCategory.WALLET),("PHONEPE",TransactionCategory.WALLET),("GPAY",TransactionCategory.WALLET),("INTEREST CREDIT",TransactionCategory.INTEREST),("ATM",TransactionCategory.CASH_WITHDRAWAL),("SALARY",TransactionCategory.SALARY),("EMI",TransactionCategory.EMI),("INSURANCE",TransactionCategory.INSURANCE),("UPI",TransactionCategory.UPI)]
        for kw,c in rules:
            if kw in u: return c
        return TransactionCategory.OTHER
