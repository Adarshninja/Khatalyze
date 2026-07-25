"""
app/services/upload_service.py

Handles:
- PDF upload
- Statement ID generation
- Metadata creation
- Metadata loading
- Metadata updates
"""

from __future__ import annotations

import json
import logging
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from core.pdf_handler import PDFHandler

from fastapi import HTTPException, UploadFile

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

BASE_DIR = Path("data")

UPLOAD_DIR = BASE_DIR / "uploads"
METADATA_DIR = BASE_DIR / "metadata"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Upload PDF
# ---------------------------------------------------------

def upload_statement(
    file: UploadFile,
    password: str | None = None,
) -> dict:
    """
    Upload a bank statement and create metadata.

    Returns
    -------
    {
        "statement_id": "...",
        "status": "uploaded",
        "pdf": "...",
        "metadata": "..."
    }
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename missing."
        )

    extension = Path(file.filename).suffix.lower()

    if extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    statement_id = uuid.uuid4().hex

    stored_filename = f"{statement_id}.pdf"

    pdf_path = UPLOAD_DIR / stored_filename

    try:

        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail="Unable to save uploaded PDF."
        )

    try:
        prepared_pdf = PDFHandler.prepare_pdf(
            pdf_path,
            password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    metadata = {

        "statement_id": statement_id,

        "original_filename": file.filename,

        "stored_filename": stored_filename,

        "password": password,

        "uploaded_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "analysis_started": None,

        "analysis_completed": None,

        "status": "uploaded",

        "bank": None,

        "files": {

            "pdf": str(prepared_pdf),

            "markdown": None,

            "text": None,

            "structured": None,

            "vector_db": None

        }

    }

    metadata_path = METADATA_DIR / f"{statement_id}.json"

    with metadata_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False,
        )

    logger.info(
        "Uploaded statement %s",
        statement_id
    )

    return {

        "statement_id": statement_id,

        "status": "uploaded",

        "pdf": str(pdf_path),

        "metadata": str(metadata_path)

    }


# ---------------------------------------------------------
# Load Metadata
# ---------------------------------------------------------

def load_metadata(
    statement_id: str
) -> dict[str, Any]:

    metadata_path = (
        METADATA_DIR /
        f"{statement_id}.json"
    )

    if not metadata_path.exists():

        raise HTTPException(

            status_code=404,

            detail="Statement metadata not found."

        )

    with metadata_path.open(
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ---------------------------------------------------------
# Save Metadata
# ---------------------------------------------------------

def save_metadata(
    statement_id: str,
    metadata: dict,
) -> None:

    metadata_path = (
        METADATA_DIR /
        f"{statement_id}.json"
    )

    with metadata_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )


# ---------------------------------------------------------
# Update Metadata
# ---------------------------------------------------------

def update_metadata(
    statement_id: str,
    **updates,
) -> dict:

    metadata = load_metadata(statement_id)

    for key, value in updates.items():

        if (
            isinstance(value, dict)
            and
            isinstance(metadata.get(key), dict)
        ):

            metadata[key].update(value)

        else:

            metadata[key] = value

    save_metadata(
        statement_id,
        metadata
    )

    logger.info(
        "Metadata updated for %s",
        statement_id
    )

    return metadata


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def statement_exists(
    statement_id: str,
) -> bool:

    return (
        METADATA_DIR /
        f"{statement_id}.json"
    ).exists()