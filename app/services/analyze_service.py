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

        print("=" * 70)
        print(f"🚀 ANALYSIS STARTED: {statement_id}")
        print("=" * 70)

        metadata = load_metadata(statement_id)
        pdf_path = Path(metadata["files"]["pdf"])

        print(f"📄 PDF path: {pdf_path}")

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        update_metadata(
            statement_id,
            status="processing",
            analysis_started=datetime.now(timezone.utc).isoformat(),
        )

        try:

            # ---------------------------------------------------------
            # STEP 1 — PDF PARSING
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("📄 STEP 1: Parsing PDF")
            print("=" * 60)

            parsed_files = self.parser.parse(pdf_path)

            markdown_file = parsed_files["markdown"]
            text_file = parsed_files["text"]

            print("✅ STEP 1 COMPLETE")
            print(f"   Markdown: {markdown_file}")
            print(f"   Text:     {text_file}")

            # ---------------------------------------------------------
            # STEP 2 — STATEMENT PARSING
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("📊 STEP 2: Building FinancialReport")
            print("=" * 60)

            statement_parser = FinancialStatementParser(markdown_file)
            report = statement_parser.parse()

            print("✅ STEP 2 COMPLETE")
            print(f"   Transactions Parsed: {len(report.transactions)}")

            # ---------------------------------------------------------
            # STEP 3 — ANALYTICS
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("📈 STEP 3: Analytics")
            print("=" * 60)

            report = AnalyticsEngine(report).generate_report()

            print("✅ STEP 3 COMPLETE")

            print("KPIs:")
            print(report.kpis)

            print("Category:")
            print(report.category_analysis)

            print("Cashflow:")
            print(report.cashflow_analysis)

            # ---------------------------------------------------------
            # STEP 4 — INSIGHTS
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("💡 STEP 4: Insights")
            print("=" * 60)

            report = InsightEngine(report).generate_report()

            print("✅ STEP 4 COMPLETE")

            # ---------------------------------------------------------
            # STEP 5 — RISK
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("⚠️ STEP 5: Risk Analysis")
            print("=" * 60)

            report = RiskEngine(report).analyze()

            print("✅ STEP 5 COMPLETE")

            # ---------------------------------------------------------
            # STEP 6 — RECOMMENDATIONS
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("🎯 STEP 6: Recommendations")
            print("=" * 60)

            report = RecommendationEngine(report).generate_report()

            print("✅ STEP 6 COMPLETE")

            # ---------------------------------------------------------
            # STEP 7 — SAVE STRUCTURED REPORT
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("💾 STEP 7: Saving structured report")
            print("=" * 60)

            structured_path = Path("data/structured") / f"{statement_id}.json"
            structured_path.parent.mkdir(parents=True, exist_ok=True)

            with open(structured_path, "w", encoding="utf-8") as f:
                json.dump(
                    report.to_dict(),
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

            print("✅ STEP 7 COMPLETE")
            print(f"   Saved: {structured_path}")

            # ---------------------------------------------------------
            # STEP 8 — CREATE EMBEDDING ENGINE
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("🧠 STEP 8: Creating EmbeddingEngine")
            print("=" * 60)

            embedding_engine = EmbeddingEngine(report)

            print("✅ STEP 8 COMPLETE")

            # ---------------------------------------------------------
            # STEP 9 — GENERATE EMBEDDINGS
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("🧠 STEP 9: Generating embeddings")
            print("=" * 60)

            embedding_result = embedding_engine.generate_embeddings()

            print("✅ STEP 9 COMPLETE")

            print(
                f"   Embeddings: {len(embedding_result['embeddings'])}"
            )

            print(
                f"   Chunks: {len(embedding_result['chunks'])}"
            )

            # ---------------------------------------------------------
            # STEP 10 — CREATE VECTOR STORE
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("🗄️ STEP 10: Creating VectorStore")
            print("=" * 60)

            vector_store = VectorStore(
                EmbeddingEngine.embedding_dimension()
            )

            print("✅ STEP 10 COMPLETE")

            # ---------------------------------------------------------
            # STEP 11 — ADD EMBEDDINGS
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("🗄️ STEP 11: Adding embeddings to VectorStore")
            print("=" * 60)

            vector_store.add_embeddings(
                embedding_result["embeddings"],
                embedding_result["chunks"],
            )

            print("✅ STEP 11 COMPLETE")

            # ---------------------------------------------------------
            # STEP 12 — SAVE VECTOR STORE
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("💾 STEP 12: Saving VectorStore")
            print("=" * 60)

            vector_db_path = Path("data/vector_db") / statement_id

            vector_store.save(vector_db_path)

            print("✅ STEP 12 COMPLETE")
            print(f"   Vector DB: {vector_db_path}")

            # ---------------------------------------------------------
            # STEP 13 — MARK COMPLETED
            # ---------------------------------------------------------
            print("\n" + "=" * 60)
            print("🎉 STEP 13: Analysis completed")
            print("=" * 60)

            update_metadata(
                statement_id,
                status="completed",
                bank=str(report.account.bank)
                if report.account.bank
                else None,
                analysis_completed=datetime.now(timezone.utc).isoformat(),
                files={
                    "markdown": str(markdown_file),
                    "text": str(text_file),
                    "structured": str(structured_path),
                    "vector_db": str(vector_db_path),
                },
            )

            print("🎉 ANALYSIS COMPLETE")
            print("=" * 70)

            return report

        except Exception as e:

            print("\n" + "=" * 70)
            print("❌ ANALYSIS FAILED")
            print("=" * 70)

            print(f"Error type: {type(e).__name__}")
            print(f"Error: {e}")

            traceback.print_exc()

            try:
                update_metadata(
                    statement_id,
                    status="failed",
                    analysis_completed=datetime.now(timezone.utc).isoformat(),
                )
            except Exception as metadata_error:
                print(
                    f"⚠️ Failed to update metadata: {metadata_error}"
                )

            raise
        