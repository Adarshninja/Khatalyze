from __future__ import annotations
import json
import traceback
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
from app.services.upload_service import load_metadata, update_metadata


class AnalyzeService:

    def __init__(self):
        self.parser = StatementParser()

    def analyze(self, statement_id: str):

        metadata = load_metadata(statement_id)
        pdf_path = Path(metadata["files"]["pdf"])

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        update_metadata(
            statement_id,
            status="processing",
            analysis_started=datetime.now(timezone.utc).isoformat(),
        )

        try:
            parsed_files = self.parser.parse(pdf_path)
            markdown_file = parsed_files["markdown"]
            text_file = parsed_files["text"]

            statement_parser = FinancialStatementParser(markdown_file)
            report = statement_parser.parse()

            print(f"Transactions Parsed: {len(report.transactions)}")

            report = AnalyticsEngine(report).generate_report()
            
            print("=" * 60)
            print("KPIs")
            print(report.kpis)

            print("Category")
            print(report.category_analysis)

            print("Cashflow")
            print(report.cashflow_analysis)
            print("=" * 60)
            
            report = InsightEngine(report).generate_report()
            report = RiskEngine(report).analyze()
            report = RecommendationEngine(report).generate_report()

            structured_path = Path("data/structured") / f"{statement_id}.json"
            structured_path.parent.mkdir(parents=True, exist_ok=True)

            with open(structured_path, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, indent=4, ensure_ascii=False)

            embedding_engine = EmbeddingEngine(report)
            embedding_result = embedding_engine.generate_embeddings()

            vector_store = VectorStore(
                EmbeddingEngine.embedding_dimension()
            )

            vector_store.add_embeddings(
                embedding_result["embeddings"],
                embedding_result["chunks"],
            )

            vector_db_path = Path("data/vector_db") / statement_id
            vector_store.save(vector_db_path)

            update_metadata(
                statement_id,
                status="completed",
                bank=str(report.account.bank) if report.account.bank else None,
                analysis_completed=datetime.now(timezone.utc).isoformat(),
                files={
                    "markdown": str(markdown_file),
                    "text": str(text_file),
                    "structured": str(structured_path),
                    "vector_db": str(vector_db_path),
                },
            )

            return report

        except Exception:
            traceback.print_exc()

            update_metadata(
                statement_id,
                status="failed",
                analysis_completed=datetime.now(timezone.utc).isoformat(),
            )

            raise
