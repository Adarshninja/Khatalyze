from __future__ import annotations

from pathlib import Path

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

        rag = FinancialRAG(
            report=None,
            llm=self.llm,
            vector_db_path=vector_db,
        )

        # return rag.ask(
        #     question=question,
        #     top_k=top_k,
        # )
        
        response = rag.ask(
            question=question,
            top_k=top_k
        )
        
        import pprint
        pprint.pp(response)
        
        return response