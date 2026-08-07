from __future__ import annotations

import json
from pathlib import Path

from models.report import FinancialReport


class ReportService:
    @staticmethod
    def get_report(statement_id: str) -> FinancialReport:
        report_path = Path("data/structured") / f"{statement_id}.json"

        if not report_path.exists():
            raise FileNotFoundError(
                f"Report not found for statement '{statement_id}'."
            )

        with open(report_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return FinancialReport.from_dict(data)
    