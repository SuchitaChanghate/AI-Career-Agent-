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
# SKILL MATCHER
# ============================================================

def match_skills(
    resume_information: str,
    job_description: str
):
    """
    Compare the candidate's resume with a job description.

    Returns:
        - Match score
        - Matching skills
        - Missing skills
        - Partial matches
        - Recommendations
    """

    prompt = f"""
You are an expert technical recruiter and
AI career advisor.

Compare the candidate's resume information
with the given job description.

CANDIDATE RESUME:
{resume_information}

JOB DESCRIPTION:
{job_description}

Analyze the candidate carefully.

Return ONLY valid JSON in exactly this structure:

{{
    "match_score": 0,
    "strong_matches": [],
    "partial_matches": [],
    "missing_skills": [],
    "recommendations": []
}}

Rules:

1. match_score must be a number from 0 to 100.

2. strong_matches should contain skills clearly
   demonstrated by the candidate.

3. partial_matches should contain skills where
   the candidate has related or incomplete experience.

4. missing_skills should contain important job
   requirements that are not demonstrated in the resume.

5. recommendations should contain practical actions
   the candidate can take to improve their fit.

6. Do not invent candidate skills.

7. Base candidate skills ONLY on the resume information.

8. Keep the recommendations concise.
"""


    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise technical recruiter. "
                    "Return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )


    result = response.choices[0].message.content


    # --------------------------------------------------------
    # Convert JSON string into Python dictionary
    # --------------------------------------------------------

    try:

        return json.loads(result)

    except json.JSONDecodeError:

        return {
            "match_score": 0,
            "strong_matches": [],
            "partial_matches": [],
            "missing_skills": [],
            "recommendations": [
                "The AI returned an invalid analysis format."
            ],
            "raw_response": result
        }