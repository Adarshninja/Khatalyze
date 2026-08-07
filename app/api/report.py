from fastapi import APIRouter, HTTPException

from app.services.report_service import ReportService

router = APIRouter(
    prefix="/report",
    tags=["Report"],
)


@router.get("/{statement_id}")
async def get_report(statement_id: str):
    try:
        report = ReportService.get_report(statement_id)

        return {
            "status": "success",
            "statement_id": statement_id,
            "report": report.to_dict(),
        }

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load report: {str(e)}",
        )
        
        