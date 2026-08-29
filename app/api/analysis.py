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
        
        
from fastapi import APIRouter, HTTPException
import threading
import traceback

router = APIRouter(
    prefix="/analyze",
    tags=["Analysis"]
)

analysis_jobs = {}

def run_analysis(statement_id: str):
    print(
        f"🔥 ANALYSIS THREAD STARTED: {statement_id}",
        flush=True
    )

    try:
        print(
            "📦 Importing AnalyzeService...",
            flush=True
        )

        from app.services.analyze_service import AnalyzeService

        print(
            "✅ AnalyzeService imported successfully",
            flush=True
        )

        analysis_jobs[statement_id] = {
            "status": "processing"
        }

        print(
            f"🚀 Running AnalyzeService: {statement_id}",
            flush=True
        )

        analyze_service = AnalyzeService()

        print(
            "✅ AnalyzeService instance created",
            flush=True
        )

        report = analyze_service.analyze(statement_id)

        print(
            "✅ AnalyzeService.analyze() completed",
            flush=True
        )

        analysis_jobs[statement_id] = {
            "status": "completed",
            "report": report.to_dict()
        }

    except Exception as e:
        print(
            f"❌ BACKGROUND ANALYSIS FAILED: {type(e).__name__}: {e}",
            flush=True
        )

        traceback.print_exc()

        analysis_jobs[statement_id] = {
            "status": "failed",
            "error": f"{type(e).__name__}: {e}"
        }
        

@router.post("/{statement_id}", status_code=202)
async def analyze(statement_id: str):

    analysis_jobs[statement_id] = {
        "status": "queued"
    }

    thread = threading.Thread(
        target=run_analysis,
        args=(statement_id,),
        daemon=True
    )

    thread.start()

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