from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi import HTTPException

from app.services.upload_service import upload_statement

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "/",
    summary="Upload a bank statement"
)
async def upload_pdf(
    file: UploadFile = File(...),
    password: str | None = Form(default=None),
):
    """
    Upload a bank statement.

    Parameters
    ----------
    file:
        PDF bank statement.

    password:
        Optional password for encrypted PDFs.
    """

    try:

        result = upload_statement(
            file=file,
            password=password,
        )

        return {
            "success": True,
            "message": "Statement uploaded successfully.",
            "data": result,
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )