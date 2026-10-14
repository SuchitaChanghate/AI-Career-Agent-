import uuid

from app.rag.vector_store import search_resume

from app.interview_session import (
    start_interview,
    evaluate_answer,
    generate_next_question
)


# =========================================================
# IN-MEMORY INTERVIEW SESSIONS
# =========================================================

interview_sessions = {}


# =========================================================
# CREATE INTERVIEW
# =========================================================

def create_interview(
    job_description: str
):
    """
    Create a new interview session.

    The candidate's resume is automatically retrieved
    from the vector database.
    """

    # -----------------------------------------------------
    # SEARCH RESUME
    # -----------------------------------------------------

    resume_results = search_resume(
        "skills, projects, education, experience, "
        "technical skills, machine learning, AI, "
        "LLMs, RAG, Python, FastAPI"
    )

    if not resume_results:
        return {
            "error": (
                "No resume information was found. "
                "Please upload a resume first."
            )
        }


    resume_information = "\n\n".join(
        resume_results
    )


    # -----------------------------------------------------
    # GENERATE FIRST QUESTION
    # -----------------------------------------------------

    first_question = start_interview(
        resume_information=resume_information,
        job_description=job_description
    )


    # -----------------------------------------------------
    # CREATE SESSION
    # -----------------------------------------------------

    session_id = str(uuid.uuid4())

    interview_sessions[session_id] = {
        "resume_information": resume_information,

        "job_description": job_description,

        "current_question": first_question,

        "history": []
    }


    return {
        "session_id": session_id,

        "question": first_question,

        "question_number": 1
    }


# =========================================================
# ANSWER INTERVIEW QUESTION
# =========================================================

def answer_interview(
    session_id: str,
    answer: str
):
    """
    Evaluate the current answer and generate
    the next interview question.
    """

    # -----------------------------------------------------
    # CHECK SESSION
    # -----------------------------------------------------

    if session_id not in interview_sessions:
        return {
            "error": "Interview session not found."
        }


    session = interview_sessions[
        session_id
    ]


    current_question = session[
        "current_question"
    ]


    resume_information = session[
        "resume_information"
    ]


    job_description = session[
        "job_description"
    ]


    # -----------------------------------------------------
    # EVALUATE ANSWER
    # -----------------------------------------------------

    evaluation = evaluate_answer(
        question=current_question,
        answer=answer
    )


    # -----------------------------------------------------
    # SAVE HISTORY
    # -----------------------------------------------------

    session["history"].append(
        {
            "question": current_question,
            "answer": answer,
            "evaluation": evaluation
        }
    )


    # -----------------------------------------------------
    # GENERATE NEXT QUESTION
    # -----------------------------------------------------

    next_question = generate_next_question(
        resume_information=resume_information,

        job_description=job_description,

        previous_question=current_question,

        previous_answer=answer
    )


    # -----------------------------------------------------
    # UPDATE SESSION
    # -----------------------------------------------------

    session["current_question"] = next_question


    question_number = len(
        session["history"]
    ) + 1


    return {
        "session_id": session_id,

        "previous_question": current_question,

        "answer": answer,

        "evaluation": evaluation,

        "next_question": next_question,

        "question_number": question_number
    }


# =========================================================
# GET INTERVIEW
# =========================================================

def get_interview(
    session_id: str
):
    """
    Get the current interview session.
    """

    if session_id not in interview_sessions:
        return {
            "error": "Interview session not found."
        }


    session = interview_sessions[
        session_id
    ]


    return {
        "session_id": session_id,

        "current_question": session[
            "current_question"
        ],

        "history": session[
            "history"
        ]
    }