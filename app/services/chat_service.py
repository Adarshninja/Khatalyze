from __future__ import annotations

import json
from pathlib import Path

from models.report import FinancialReport

from app.services.upload_service import load_metadata

from core.rag import FinancialRAG
from core.llm import LLMClient


class ChatService:

    def __init__(self):
        self.llm = LLMClient()

    def chat(
        self,
        statement_id: str,
        question: str,
        top_k: int = 5,
    ):

        metadata = load_metadata(statement_id)

        vector_db = metadata["files"]["vector_db"]

        if not vector_db:
            raise FileNotFoundError(
                "Vector database not found. Please analyze the statement first."
            )

        if not Path(vector_db).exists():
            raise FileNotFoundError(
                f"Vector database does not exist: {vector_db}"
            )

        # Load FinancialReport
        structured_path = metadata["files"]["structured"]

        if not Path(structured_path).exists():
            raise FileNotFoundError(
                f"Structured report not found: {structured_path}"
            )

        with open(structured_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)

        report = FinancialReport.from_dict(report_data)

        # Create RAG
        rag = FinancialRAG(
            report=report,
            llm=self.llm,
            vector_db_path=vector_db,
        )

        # Ask question
        response = rag.ask(
            question=question,
            top_k=top_k,
        )

        return response