from __future__ import annotations

import json

from app.services.upload_service import METADATA_DIR
from app.services.report_service import ReportService


class StatementsService:
    @staticmethod
    def list_statements() -> list[dict]:
        statements: list[dict] = []

        for metadata_file in METADATA_DIR.glob("*.json"):

            with metadata_file.open("r", encoding="utf-8") as f:
                metadata = json.load(f)

            if metadata.get("status") != "completed":
                continue

            statement_id = metadata["statement_id"]

            try:
                report = ReportService.get_report(statement_id)
            except Exception:
                continue

            statements.append(
    {
        "statement_id": statement_id,

        "bank": (
            report.account.bank.value.replace("_", " ").title()
            if report.account.bank
            else "Unknown Bank"
        ),

        "transaction_count": report.total_transactions,

        "health_score": report.financial_health_score,

        "health_status": report.financial_health_status,

        "uploaded_at": metadata.get("uploaded_at"),

        "analysis_completed": metadata.get("analysis_completed"),

        "original_filename": metadata.get("original_filename"),

        "status": metadata.get("status"),
    }
)

        statements.sort(
            key=lambda x: x["uploaded_at"] or "",
            reverse=True,
        )

        return statements
    