import json
import os

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# GENERATE INTERVIEW QUESTIONS
# ============================================================

def generate_interview(
    resume_information: str,
    job_description: str
):
    """
    Generate personalized interview questions based on
    the candidate's resume and the target job.
    """

    prompt = f"""
You are a senior technical interviewer.

Create a personalized interview for the candidate
based on their resume and the target job description.

CANDIDATE RESUME:
{resume_information}

JOB DESCRIPTION:
{job_description}

Generate questions in these categories:

1. Technical Questions
2. Project Questions
3. AI/ML Questions
4. Behavioral/HR Questions

Return ONLY valid JSON using this structure:

{{
    "technical_questions": [],
    "project_questions": [],
    "ai_ml_questions": [],
    "behavioral_questions": []
}}

Rules:

- Questions must be relevant to the job.
- Questions should be based on the candidate's actual resume.
- Do not invent projects or experience.
- Include questions about technologies mentioned
  in the job description.
- Make the questions appropriate for an AI Engineer interview.
"""


    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior AI Engineer interviewer. "
                    "Return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )


    result = response.choices[0].message.content


    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "technical_questions": [],
            "project_questions": [],
            "ai_ml_questions": [],
            "behavioral_questions": [],
            "raw_response": result
        }