import re

class TransactionNormalizer:

    @staticmethod
    def normalize(txn: dict):

        description = txn["description"].strip()

        normalized = txn.copy()

        normalized["mode"] = TransactionNormalizer.detect_mode(description)

        normalized["reference_number"] = TransactionNormalizer.detect_reference(description)

        normalized["party"] = TransactionNormalizer.detect_party(description)

        normalized["bank"] = TransactionNormalizer.detect_bank(description)

        normalized["category"] = TransactionNormalizer.detect_category(description)

        return normalized

    @staticmethod
    def detect_mode(text):

        if text.startswith("UPI"):
            return "UPI"

        if text.startswith("ATM"):
            return "ATM"

        if text.startswith("NEFT"):
            return "NEFT"

        if text.startswith("IMPS"):
            return "IMPS"

        if text.startswith("RTGS"):
            return "RTGS"

        if "INTEREST CREDIT" in text.upper():
            return "INTEREST"

        return "OTHER"

    @staticmethod
    def detect_reference(text):

        match = re.search(r"/(\d{6,})/", text)

        if match:
            return match.group(1)

        return ""

    @staticmethod
    def detect_party(text):

        parts = text.split("/")

        if len(parts) >= 4:
            return parts[3].strip()

        return ""

    @staticmethod
    def detect_bank(text):

        banks = [
            "SBIN",
            "PUNB",
            "HDFC",
            "ICIC",
            "YESB",
            "BARB",
            "IDIB",
            "UTIB",
            "KKBK",
            "AIRP",
            "NSPB",
            "IPOS",
            "INDB"
        ]

        upper = text.upper()

        for bank in banks:

            if bank in upper:
                return bank

        return ""

    @staticmethod
    def detect_category(text):

        text = text.upper()

        if "GROWW" in text:
            return "Investment"

        if "BHARATPE" in text:
            return "Merchant Payment"

        if "PAYTM" in text:
            return "Wallet"

        if "INTEREST CREDIT" in text:
            return "Interest"

        if "ATM" in text:
            return "Cash Withdrawal"

        if "UPI" in text:
            return "UPI"

        return "Other"
