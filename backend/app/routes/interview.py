from fastapi import APIRouter
from pydantic import BaseModel

from app.interview_manager import (
    create_interview,
    answer_interview,
    get_interview
)


router = APIRouter(
    prefix="/api/interview",
    tags=["Interview"]
)


# =========================================================
# REQUEST MODELS
# =========================================================

class StartInterviewRequest(BaseModel):
    job_description: str


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


# =========================================================
# START INTERVIEW
# =========================================================

@router.post("/start")
def start(
    request: StartInterviewRequest
):
    return create_interview(
        job_description=request.job_description
    )


# =========================================================
# ANSWER QUESTION
# =========================================================

@router.post("/answer")
def answer(
    request: AnswerRequest
):
    return answer_interview(
        session_id=request.session_id,
        answer=request.answer
    )


# =========================================================
# GET INTERVIEW
# =========================================================

@router.get("/{session_id}")
def get_session(
    session_id: str
):
    return get_interview(
        session_id=session_id
    )