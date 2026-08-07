from fastapi import APIRouter, HTTPException

from app.services.analyze_service import AnalyzeService

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

analyze_service = AnalyzeService()


@router.post("/{statement_id}")
async def analyze(statement_id: str):

    try:

        report = analyze_service.analyze(statement_id)

        return {
            "status": "success",
            "statement_id": statement_id,
            "message": "Statement analyzed successfully.",
            "report": report.to_dict()
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
        
        