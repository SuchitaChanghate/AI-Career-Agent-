import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from app.rag.vector_store import search_resume
from app.interview_agent import generate_interview
from app.interview_session import (
    start_interview,
    evaluate_answer,
    generate_next_question
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# TOOL 1 — SEARCH RESUME
# =========================================================

def search_resume_tool(query: str):
    """
    Search the uploaded resume and return
    relevant information.
    """

    results = search_resume(query)

    if not results:
        return "No relevant information was found in the resume."

    return "\n\n".join(results)
def get_resume_profile():
    """
    Load the structured resume JSON.

    The JSON file is the primary source of truth
    for structured candidate information.
    """

    resume_path = Path("resume_data/resume.json")

    if not resume_path.exists():
        return {
            "error": (
                "No structured resume was found. "
                "Please upload a resume first."
            )
        }

    try:
        with open(
            resume_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except json.JSONDecodeError:
        return {
            "error": (
                "The resume JSON file is invalid."
            )
        }

    except Exception as error:
        return {
            "error": (
                f"Could not load resume profile: {error}"
            )
        }


# =========================================================
# TOOL 2 — ANALYZE JOB DESCRIPTION
# =========================================================

def analyze_job_description(job_description: str):
    """
    Analyze a job description and extract:
    - Job title
    - Required skills
    - Preferred skills
    - Experience
    - Responsibilities
    - Education requirements
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are an expert job description analyzer.

Analyze the given job description.

Extract the following information:

1. Job Title
2. Required Technical Skills
3. Preferred Technical Skills
4. Required Experience
5. Important Responsibilities
6. Education Requirements
7. Other Important Requirements

Return the result in a clear and structured format.

Do NOT invent information.

Only use information that is actually
present in the job description.
"""
            },
            {
                "role": "user",
                "content": job_description
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content


# =========================================================
# TOOL 3 — GENERATE INTERVIEW QUESTIONS
# =========================================================

def generate_interview_tool(
    resume_information: str,
    job_description: str
):
    """
    Generate personalized interview questions
    based on the candidate's resume and job description.
    """

    return generate_interview(
        resume_information=resume_information,
        job_description=job_description
    )

# =========================================================
# TOOL 5 — START INTERVIEW
# =========================================================

def start_interview_tool(
    resume_information: str,
    job_description: str
):
    """
    Start an interactive interview.
    """

    return start_interview(
        resume_information=resume_information,
        job_description=job_description
    )


# =========================================================
# TOOL 6 — EVALUATE INTERVIEW ANSWER
# =========================================================

def evaluate_answer_tool(
    question: str,
    answer: str
):
    """
    Evaluate the candidate's interview answer.
    """

    return evaluate_answer(
        question=question,
        answer=answer
    )


# =========================================================
# TOOL 7 — GENERATE NEXT QUESTION
# =========================================================

def generate_next_question_tool(
    resume_information: str,
    job_description: str,
    previous_question: str,
    previous_answer: str
):
    """
    Generate the next interview question.
    """

    return generate_next_question(
        resume_information=resume_information,
        job_description=job_description,
        previous_question=previous_question,
        previous_answer=previous_answer
    )