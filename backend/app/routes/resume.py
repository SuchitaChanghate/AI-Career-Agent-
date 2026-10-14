import json
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.rag.loader import extract_text_from_pdf, chunk_text
from app.rag.vector_store import store_resume
from app.resume_parser import extract_resume_json


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"]
)


# ============================================================
# DIRECTORIES
# ============================================================

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

RESUME_DATA_DIR = Path("resume_data")
RESUME_DATA_DIR.mkdir(exist_ok=True)


# ============================================================
# UPLOAD RESUME
# ============================================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):
    """
    Upload a PDF resume, extract its text, create RAG chunks,
    generate structured resume JSON, and save it.
    """

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename:
        return {
            "error": "No file was selected."
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF resumes are supported."
        }

    # --------------------------------------------------------
    # Save uploaded PDF
    # --------------------------------------------------------

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as error:
        return {
            "error": f"Could not save the uploaded resume: {error}"
        }

    # --------------------------------------------------------
    # Extract text from PDF
    # --------------------------------------------------------

    try:
        text = extract_text_from_pdf(
            str(file_path)
        )

    except Exception as error:
        return {
            "error": f"Could not extract text from the resume: {error}"
        }

    if not text.strip():
        return {
            "error": "No readable text was found in the PDF."
        }

    # --------------------------------------------------------
    # Create chunks for RAG
    # --------------------------------------------------------

    try:
        chunks = chunk_text(text)

        number_of_chunks = store_resume(
            chunks
        )

    except Exception as error:
        return {
            "error": f"Could not process resume for RAG: {error}"
        }

    # --------------------------------------------------------
    # Extract structured resume JSON
    # --------------------------------------------------------

    try:
        resume_json = extract_resume_json(
            text
        )

    except Exception as error:
        return {
            "error": f"Resume JSON extraction failed: {error}"
        }

    # --------------------------------------------------------
    # Check parser result
    # --------------------------------------------------------

    if not isinstance(resume_json, dict):
        return {
            "error": "Resume parser did not return valid JSON."
        }

    if "error" in resume_json:
        return {
            "error": "Resume extraction failed.",
            "details": resume_json
        }

    # --------------------------------------------------------
    # Save structured resume
    # --------------------------------------------------------

    json_path = RESUME_DATA_DIR / "resume.json"

    try:
        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as json_file:

            json.dump(
                resume_json,
                json_file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:
        return {
            "error": f"Could not save resume profile: {error}"
        }

    # --------------------------------------------------------
    # Return successful response
    # --------------------------------------------------------

    return {
        "message": "Resume processed successfully.",
        "filename": file.filename,
        "characters_extracted": len(text),
        "chunks_created": number_of_chunks,
        "resume": resume_json
    }


# ============================================================
# GET STRUCTURED RESUME PROFILE
# ============================================================

@router.get("/profile")
def get_resume_profile():
    """
    Return the structured resume JSON.

    This endpoint is used by the frontend Resume Dashboard
    and can also be used by other AI Career Agent components.
    """

    json_path = RESUME_DATA_DIR / "resume.json"

    # --------------------------------------------------------
    # Check whether resume exists
    # --------------------------------------------------------

    if not json_path.exists():
        return {
            "error": "No resume profile found. Please upload your resume first."
        }

    # --------------------------------------------------------
    # Read JSON
    # --------------------------------------------------------

    try:
        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as json_file:

            resume_data = json.load(
                json_file
            )

        return resume_data

    # --------------------------------------------------------
    # Invalid JSON
    # --------------------------------------------------------

    except json.JSONDecodeError:
        return {
            "error": "The resume JSON file is invalid."
        }

    # --------------------------------------------------------
    # Other errors
    # --------------------------------------------------------

    except Exception as error:
        return {
            "error": f"Could not load resume profile: {error}"
        }