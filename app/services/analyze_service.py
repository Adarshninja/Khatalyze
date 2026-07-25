from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from core.parser import StatementParser
from core.statement_parser import StatementParser as FinancialStatementParser

from core.analytics import AnalyticsEngine
from core.insights import InsightEngine
from core.risk_engine import RiskEngine
from core.recommendation_engine import RecommendationEngine
from core.embeddings import EmbeddingEngine
from core.vector_store import VectorStore

from app.services.upload_service import (
    load_metadata,
    update_metadata,
)


class AnalyzeService:

    def __init__(self):
        self.parser = StatementParser()

    def analyze(self, statement_id: str):

        ####################################################
        # Load metadata
        ####################################################

        metadata = load_metadata(statement_id)

        pdf_path = Path(metadata["files"]["pdf"])

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        ####################################################
        # Mark analysis started
        ####################################################

        update_metadata(
            statement_id,
            status="processing",
            analysis_started=datetime.now(
                timezone.utc
            ).isoformat()
        )

        try:

            ####################################################
            # Step 1 : Parse PDF
            ####################################################

            parsed_files = self.parser.parse(pdf_path)

            markdown_file = parsed_files["markdown"]
            text_file = parsed_files["text"]

            ####################################################
            # Step 2 : Markdown -> FinancialReport
            ####################################################

            statement_parser = FinancialStatementParser(
                markdown_file
            )

            report = statement_parser.parse()

            ####################################################
            # Step 3 : Save Structured JSON
            ####################################################

            structured_path = (
                Path("data/structured")
                / f"{statement_id}.json"
            )

            statement_parser.save(
                structured_path
            )

            ####################################################
            # Step 4 : Analytics
            ####################################################

            report = AnalyticsEngine(
                report
            ).generate_report()

            ####################################################
            # Step 5 : Insights
            ####################################################

            report = InsightEngine(
                report
            ).generate_report()

            ####################################################
            # Step 6 : Risks
            ####################################################

            report = RiskEngine(
                report
            ).analyze()

            ####################################################
            # Step 7 : Recommendations
            ####################################################

            report = RecommendationEngine(
                report
            ).generate_report()

            ####################################################
            # Step 8 : Embeddings
            ####################################################

            embedding_engine = EmbeddingEngine(
                report
            )

            embedding_result = (
                embedding_engine.generate_embeddings()
            )

            ####################################################
            # Step 9 : Vector Store
            ####################################################

            vector_store = VectorStore(
                EmbeddingEngine.embedding_dimension()
            )

            vector_store.add_embeddings(
                embedding_result["embeddings"],
                embedding_result["chunks"]
            )
            
            vector_db_path = (
                Path("data/vector_db")
                / statement_id
            )

            vector_store.save(vector_db_path)

            ####################################################
            # Step 10 : Update Metadata
            ####################################################

            update_metadata(
                statement_id,
                status="completed",
                bank=str(report.account.bank)
                if report.account.bank
                else None,
                analysis_completed=datetime.now(
                    timezone.utc
                ).isoformat(),
                files={
                    "markdown": str(markdown_file),
                    "text": str(text_file),
                    "structured": str(structured_path),
                    "vector_db": str(vector_db_path),
                }
            )

            ####################################################
            # Done
            ####################################################

            return report

        except Exception:

            update_metadata(
                statement_id,
                status="failed",
                analysis_completed=datetime.now(
                    timezone.utc
                ).isoformat()
            )

            raise