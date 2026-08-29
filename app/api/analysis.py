# from fastapi import APIRouter, HTTPException

# router = APIRouter(
#     prefix="/analyze",
#     tags=["Analysis"]
# )


# @router.post("/{statement_id}")
# async def analyze(statement_id: str):

#     try:
#         from app.services.analyze_service import AnalyzeService
#         analyze_service = AnalyzeService()

#         report = analyze_service.analyze(statement_id)

#         return {
#             "status": "success",
#             "statement_id": statement_id,
#             "message": "Statement analyzed successfully.",
#             "report": report.to_dict()
#         }

#     except FileNotFoundError as e:

#         raise HTTPException(
#             status_code=404,
#             detail=str(e)
#         )

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=f"Analysis failed: {str(e)}"
#         )
        
        
        
from fastapi import APIRouter, HTTPException, BackgroundTasks

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

analysis_jobs = {}


def run_analysis(statement_id: str):
    try:
        from app.services.analyze_service import AnalyzeService

        analysis_jobs[statement_id] = {
            "status": "processing"
        }

        analyze_service = AnalyzeService()
        report = analyze_service.analyze(statement_id)

        analysis_jobs[statement_id] = {
            "status": "completed",
            "report": report.to_dict()
        }

    except FileNotFoundError as e:
        analysis_jobs[statement_id] = {
            "status": "failed",
            "error": str(e)
        }

    except Exception as e:
        analysis_jobs[statement_id] = {
            "status": "failed",
            "error": str(e)
        }


@router.post("/{statement_id}", status_code=202)
async def analyze(
    statement_id: str,
    background_tasks: BackgroundTasks
):
    analysis_jobs[statement_id] = {
        "status": "queued"
    }

    background_tasks.add_task(
        run_analysis,
        statement_id
    )

    return {
        "status": "processing",
        "statement_id": statement_id,
        "message": "Analysis started."
    }


@router.get("/{statement_id}/status")
async def analysis_status(statement_id: str):

    job = analysis_jobs.get(statement_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis job not found."
        )

    return {
        "statement_id": statement_id,
        **job
    }