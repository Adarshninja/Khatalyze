from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)


@router.post("/{statement_id}")
async def analyze(statement_id: str):

    try:
        from app.services.analyze_service import AnalyzeService
        analyze_service = AnalyzeService()

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
        
        