import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


RESUME_SCHEMA = {
    "personal_information": {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "github": ""
    },

    "summary": "",

    "education": [],

    "skills": {
        "programming_languages": [],
        "frameworks": [],
        "libraries": [],
        "databases": [],
        "ai_ml": [],
        "cloud": [],
        "tools": [],
        "other": []
    },

    "experience": [],

    "projects": [],

    "certifications": [],

    "achievements": [],

    "languages": []
}


def extract_resume_json(resume_text: str):

    prompt = f"""
You are a professional resume parser.

Your job is to convert the resume text into structured JSON.

IMPORTANT RULES:

1. Use ONLY information explicitly present in the resume.
2. NEVER invent information.
3. NEVER assume a skill just because another skill is present.
4. Preserve the candidate's actual project names.
5. Preserve actual technologies mentioned.
6. If information is missing, use an empty string or empty array.
7. Do not add explanations.
8. Return ONLY valid JSON.
9. Do not use Markdown code fences.
10. Do not add comments.
11. Do not infer years of experience.
12. Do not infer skills from job titles.
13. Keep projects separate.
14. Keep education separate.
15. Keep professional experience separate from projects.

Use exactly this JSON structure:

{json.dumps(RESUME_SCHEMA, indent=2)}

RESUME TEXT:

{resume_text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are a highly accurate resume information extraction
system.

Your responsibility is information extraction,
NOT career advice.

You must never hallucinate information.

Return valid JSON only.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    # Remove accidental markdown fences
    if result.startswith("```json"):
        result = result[7:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    try:
        parsed_resume = json.loads(result)
        return parsed_resume

    except json.JSONDecodeError:
        return {
            "error": "Resume could not be converted to valid JSON.",
            "raw_response": result
        }