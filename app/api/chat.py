from pydantic import BaseModel

from fastapi import APIRouter
from fastapi import HTTPException

from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

chat_service = ChatService()


class ChatRequest(BaseModel):
    question: str
    top_k: int = 5


@router.post("/{statement_id}")
async def chat(
    statement_id: str,
    request: ChatRequest,
):

    try:

        response = chat_service.chat(
            statement_id=statement_id,
            question=request.question,
            top_k=request.top_k,
        )

        return {
            "status": "success",
            "statement_id": statement_id,
            **response,
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )