import json

from fastapi import APIRouter
from pydantic import BaseModel

from app.tools import (
    get_resume_profile,
    analyze_job_description
)

from app.skill_matcher import match_skills


router = APIRouter(
    prefix="/api/job-match",
    tags=["Job Match"]
)


# =========================================================
# REQUEST MODEL
# =========================================================

class JobMatchRequest(BaseModel):

    job_description: str


# =========================================================
# JOB MATCH ENDPOINT
# =========================================================

@router.post("/")
def analyze_job_match(
    request: JobMatchRequest
):

    # -----------------------------------------------------
    # Validate job description
    # -----------------------------------------------------

    if not request.job_description.strip():

        return {
            "error": "Job description cannot be empty."
        }


    # -----------------------------------------------------
    # Get structured resume
    # -----------------------------------------------------

    resume_profile = get_resume_profile()


    if "error" in resume_profile:

        return {
            "error": (
                "Please upload your resume before "
                "analyzing a job."
            )
        }


    # -----------------------------------------------------
    # Convert resume JSON to text
    # -----------------------------------------------------

    resume_information = json.dumps(
        resume_profile,
        ensure_ascii=False,
        indent=2
    )


    # -----------------------------------------------------
    # Analyze job description
    # -----------------------------------------------------

    job_analysis = analyze_job_description(
        request.job_description
    )


    # -----------------------------------------------------
    # Match resume with job
    # -----------------------------------------------------

    match_result = match_skills(
        resume_information=resume_information,
        job_description=request.job_description
    )


    # -----------------------------------------------------
    # Return complete result
    # -----------------------------------------------------

    return {
        "job_analysis": job_analysis,
        "match_result": match_result
    }