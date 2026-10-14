import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# START INTERVIEW
# =========================================================

def start_interview(
    resume_information: str,
    job_description: str
):
    """
    Start an interactive AI interview.

    The AI generates the first interview question
    based on the candidate's resume and job description.
    """

    prompt = f"""
You are a professional AI Engineer interviewer.

You are conducting a technical interview.

CANDIDATE RESUME:
{resume_information}

JOB DESCRIPTION:
{job_description}

Your task is to start the interview.

Rules:

1. Ask ONLY ONE question.

2. The first question should be appropriate
   for an AI Engineer interview.

3. Prefer questions related to the candidate's
   actual experience, projects, or skills.

4. Do not ask multiple questions.

5. Do not provide the answer.

6. Do not provide feedback yet.

Return only the interview question.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional technical interviewer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# =========================================================
# EVALUATE ANSWER
# =========================================================

def evaluate_answer(
    question: str,
    answer: str
):
    """
    Evaluate the candidate's answer.
    """

    prompt = f"""
You are an experienced AI Engineer interviewer.

Evaluate the candidate's answer.

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{answer}

Evaluate the answer based on:

1. Technical correctness
2. Understanding
3. Clarity
4. Completeness
5. Practical knowledge

Return the result in this format:

Score: X/10

What was good:
- ...

What could be improved:
- ...

Ideal answer:
- ...

Keep the feedback concise and useful.

Do not invent facts about the candidate.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict but helpful technical interviewer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# =========================================================
# NEXT QUESTION
# =========================================================

def generate_next_question(
    resume_information: str,
    job_description: str,
    previous_question: str,
    previous_answer: str
):
    """
    Generate the next interview question based on
    the previous question and candidate answer.
    """

    prompt = f"""
You are conducting an AI Engineer technical interview.

CANDIDATE RESUME:
{resume_information}

JOB DESCRIPTION:
{job_description}

PREVIOUS QUESTION:
{previous_question}

CANDIDATE ANSWER:
{previous_answer}

Generate the next interview question.

Rules:

1. Ask ONLY ONE question.

2. Do not repeat the previous question.

3. The question should become progressively
   more relevant and challenging.

4. Cover different areas such as:

   - Python
   - Machine Learning
   - Deep Learning
   - LLMs
   - RAG
   - FastAPI
   - Databases
   - AI Agents
   - System Design
   - Projects

5. Prefer questions related to the candidate's
   actual resume.

6. Do not provide the answer.

Return only the next interview question.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional AI Engineer interviewer."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content