from fastapi import APIRouter

from app.services.statements_service import StatementsService

router = APIRouter(
    prefix="/statements",
    tags=["Statements"],
)


@router.get("")
def list_statements():
    return {
        "status": "success",
        "statements": StatementsService.list_statements(),
    }
    