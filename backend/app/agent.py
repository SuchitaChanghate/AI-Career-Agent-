import json
import os

from dotenv import load_dotenv
from groq import Groq

from app.tools import (
    search_resume_tool,
    get_resume_profile,
    analyze_job_description,
    generate_interview_tool,
    start_interview_tool,
    evaluate_answer_tool,
    generate_next_question_tool
)

from app.skill_matcher import match_skills


# =========================================================
# GROQ CLIENT
# =========================================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================================================
# AI AGENT TOOLS
# =========================================================

tools = [

    # =====================================================
    # TOOL 1 — SEARCH RESUME
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "search_resume",
            "description": (
                "Search the user's uploaded resume for "
                "skills, projects, education, experience, "
                "certifications, achievements, or other "
                "relevant information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The specific information you want "
                            "to find in the user's resume."
                        )
                    }
                },
                "required": ["query"]
            }
        }
    },
        # =====================================================
    # TOOL 2 — GET STRUCTURED RESUME
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "get_resume_profile",
            "description": (
                "Get the complete structured resume profile "
                "from the uploaded resume JSON. Use this for "
                "exact candidate information such as skills, "
                "education, projects, experience, "
                "certifications and achievements."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    # =====================================================
    # TOOL 2 — ANALYZE JOB DESCRIPTION
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "analyze_job_description",
            "description": (
                "Analyze a job description and extract "
                "job title, required skills, preferred "
                "skills, experience, responsibilities "
                "and education requirements."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "job_description": {
                        "type": "string",
                        "description": (
                            "The complete job description "
                            "that needs to be analyzed."
                        )
                    }
                },
                "required": ["job_description"]
            }
        }
    },

    # =====================================================
    # TOOL 3 — MATCH SKILLS
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "match_skills",
            "description": (
                "Compare the candidate's resume information "
                "with a job description and determine the "
                "candidate's match score, strong matches, "
                "partial matches, missing skills and "
                "recommendations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_information": {
                        "type": "string",
                        "description": (
                            "Relevant information retrieved "
                            "from the candidate's resume."
                        )
                    },
                    "job_description": {
                        "type": "string",
                        "description": (
                            "The job description to compare "
                            "against the candidate."
                        )
                    }
                },
                "required": [
                    "resume_information",
                    "job_description"
                ]
            }
        }
    },

    # =====================================================
    # TOOL 4 — GENERATE INTERVIEW
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "generate_interview",
            "description": (
                "Generate personalized interview questions "
                "based on the candidate's resume and job "
                "description."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_information": {
                        "type": "string",
                        "description": (
                            "Relevant information retrieved "
                            "from the candidate's resume."
                        )
                    },
                    "job_description": {
                        "type": "string",
                        "description": (
                            "The target job description."
                        )
                    }
                },
                "required": [
                    "resume_information",
                    "job_description"
                ]
            }
        }
    },

    # =====================================================
    # TOOL 5 — START INTERVIEW
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "start_interview",
            "description": (
                "Start an interactive AI Engineer interview "
                "and ask the first interview question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_information": {
                        "type": "string",
                        "description": (
                            "Relevant information from the "
                            "candidate's resume."
                        )
                    },
                    "job_description": {
                        "type": "string",
                        "description": (
                            "The target job description."
                        )
                    }
                },
                "required": [
                    "resume_information",
                    "job_description"
                ]
            }
        }
    },

    # =====================================================
    # TOOL 6 — EVALUATE ANSWER
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "evaluate_answer",
            "description": (
                "Evaluate the candidate's answer to an "
                "interview question and provide a score, "
                "feedback and ideal answer."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": (
                            "The interview question."
                        )
                    },
                    "answer": {
                        "type": "string",
                        "description": (
                            "The candidate's answer."
                        )
                    }
                },
                "required": [
                    "question",
                    "answer"
                ]
            }
        }
    },

    # =====================================================
    # TOOL 7 — GENERATE NEXT QUESTION
    # =====================================================

    {
        "type": "function",
        "function": {
            "name": "generate_next_question",
            "description": (
                "Generate the next personalized interview "
                "question based on the previous question "
                "and candidate answer."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resume_information": {
                        "type": "string",
                        "description": (
                            "Relevant information from the "
                            "candidate's resume."
                        )
                    },
                    "job_description": {
                        "type": "string",
                        "description": (
                            "The target job description."
                        )
                    },
                    "previous_question": {
                        "type": "string",
                        "description": (
                            "The previous interview question."
                        )
                    },
                    "previous_answer": {
                        "type": "string",
                        "description": (
                            "The candidate's previous answer."
                        )
                    }
                },
                "required": [
                    "resume_information",
                    "job_description",
                    "previous_question",
                    "previous_answer"
                ]
            }
        }
    }
]


# =========================================================
# MAIN AI AGENT
# =========================================================

def run_agent(
    user_message: str,
    chat_history=None
):

    """
    Run the AI Career Agent.

    chat_history allows the agent to remember
    previous messages in the current conversation.
    """

    if chat_history is None:
        chat_history = []


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    system_prompt = """
You are an AI Career Agent.

You help the candidate with:

- Resume analysis
- Skills
- Projects
- Education
- Experience
- Job descriptions
- Job matching
- Skill gaps
- Career recommendations
- Interview preparation
- Interactive technical interviews

You are NOT a generic chatbot.

You are a professional AI career assistant
whose answers must be grounded in the candidate's
actual resume whenever the question is
candidate-specific.


=========================================================
RESUME GROUNDING
=========================================================

The uploaded resume is the primary source of truth
for candidate-specific information.

When the user asks about their:

- Skills
- Projects
- Education
- Experience
- Technologies
- Certifications
- Achievements
- Programming languages
- Frameworks
- Databases
- AI/ML knowledge

use the search_resume tool.

Do NOT guess.

Do NOT invent information.

Do NOT assume a skill just because it is related
to another skill.

For example:

If the resume contains Python, do NOT automatically
claim that the candidate knows Django.

If the resume contains Machine Learning, do NOT
automatically claim that the candidate knows
Deep Learning.

Only claim what is supported by the resume.


=========================================================
WHEN INFORMATION IS NOT AVAILABLE
=========================================================

If the requested information cannot be found
in the resume, clearly say:

"I couldn't find that information in your resume."

Never fabricate:

- Experience
- Skills
- Projects
- Companies
- Technologies
- Certifications
- Education
- Years of experience
- Job titles
- Achievements


=========================================================
RESUME SEARCH
=========================================================

Use search_resume whenever the user asks
candidate-specific questions.

Examples:

"What skills do I have?"

"What projects are on my resume?"

"Do I know Python?"

"Have I worked with FastAPI?"

"What technologies did I use?"

"What AI projects have I built?"

"What is my education?"

"What experience do I have?"

"What are my strongest skills?"


=========================================================
FACTS VS RECOMMENDATIONS
=========================================================

Clearly separate information from the resume
and your recommendations.

Example:

Based on your resume:

- Python
- FastAPI
- Machine Learning
- RAG

My recommendation:

- Learn Docker
- Learn cloud deployment
- Build a production RAG application

Do not present recommendations as existing
candidate skills.


=========================================================
JOB DESCRIPTION ANALYSIS
=========================================================

When the user provides a job description,
use analyze_job_description.

Extract:

- Job title
- Required technical skills
- Preferred skills
- Experience requirements
- Responsibilities
- Education requirements
- Other important requirements

Do not invent requirements.


=========================================================
JOB MATCHING
=========================================================

When the user asks:

"Am I suitable for this job?"

"How well do I match?"

"What skills am I missing?"

"Should I apply?"

"Compare my resume with this job."

use:

1. search_resume
2. analyze_job_description if necessary
3. match_skills

The matching result should distinguish:

STRONG MATCH
The resume clearly demonstrates the skill.

PARTIAL MATCH
The resume demonstrates related knowledge,
but not the exact requirement.

MISSING SKILL
The resume does not demonstrate the requirement.

Never call something a strong match without
evidence from the resume.


=========================================================
MATCH SCORE
=========================================================

If match_skills returns a score, describe it as
an AI-generated estimate.

Do NOT describe it as:

- Probability of getting hired
- Guaranteed interview chance
- Guaranteed selection

Example:

"Your estimated skill match is 63%.

This score reflects how closely the skills
demonstrated in your resume align with the
job description."


=========================================================
CAREER RECOMMENDATIONS
=========================================================

Career recommendations should be practical
and based on the candidate's current skills.

For example:

"Your resume already demonstrates Python,
FastAPI, Machine Learning and RAG.

For an AI Engineer role, I recommend prioritizing:

1. Docker
2. Cloud deployment
3. Vector databases
4. Production RAG
5. AI agent architecture"


=========================================================
INTERVIEW PREPARATION
=========================================================

When the user asks for interview preparation,
use the appropriate interview tools.

Questions should preferably be based on:

- Candidate's resume
- Candidate's projects
- Target job description
- Python
- Machine Learning
- Deep Learning
- LLMs
- RAG
- FastAPI
- Databases
- AI Agents
- System Design

Do not invent candidate experience.


=========================================================
INTERACTIVE INTERVIEW
=========================================================

When conducting an interactive interview:

1. Ask ONE question at a time.

2. Prefer questions based on the candidate's
   actual resume and projects.

3. After the candidate answers:

   - Evaluate the answer.
   - Give a score.
   - Explain what was good.
   - Explain what needs improvement.
   - Give an ideal answer.
   - Generate the next question.

4. Gradually increase difficulty.

5. Do not repeat questions unnecessarily.


=========================================================
CONVERSATION MEMORY
=========================================================

Use previous conversation history to understand
follow-up questions.

For example:

User:
"What skill should I improve first?"

User:
"Why?"

Understand that "Why?" refers to the
previous recommendation.

However, conversation history must NOT override
verified resume information.

If conversation history conflicts with the resume,
prefer the resume.


=========================================================
TOOL USAGE
=========================================================

Available tools:

1. search_resume
2. analyze_job_description
3. match_skills
4. generate_interview
5. start_interview
6. evaluate_answer
7. generate_next_question

Use the appropriate tool when needed.

Do not call tools unnecessarily.

For candidate-specific resume questions,
prefer search_resume instead of guessing.


=========================================================
RESPONSE STYLE
=========================================================

Be:

- Accurate
- Clear
- Concise
- Practical
- Professional
- Honest

For simple questions:
give a simple answer.

For technical questions:
explain clearly with examples.

For career questions:
give actionable recommendations.

Do not produce unnecessarily long answers.


=========================================================
MOST IMPORTANT RULE
=========================================================

NEVER HALLUCINATE CANDIDATE INFORMATION.

If you do not know something about the candidate,
search the resume.

If the information still cannot be found,
say that it is not available.

Accuracy is more important than confidence.
"""


    # =====================================================
    # INITIAL CONVERSATION
    # =====================================================

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # =====================================================
    # ADD PREVIOUS CHAT HISTORY
    # =====================================================

    for message in chat_history:

        role = message.get("role")
        content = message.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not content:
            continue

        messages.append(
            {
                "role": role,
                "content": content
            }
        )


    # =====================================================
    # ADD CURRENT USER MESSAGE
    # =====================================================

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # =====================================================
    # TOOL-CALL LOOP
    # =====================================================

    max_iterations = 6

    for _ in range(max_iterations):

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )

        message = response.choices[0].message


        # =================================================
        # AI HAS FINISHED
        # =================================================

        if not message.tool_calls:

            return (
                message.content
                or "I couldn't generate a response."
            )


        # =================================================
        # ADD ASSISTANT TOOL CALL
        # =================================================

        messages.append(message)


        # =================================================
        # EXECUTE TOOLS
        # =================================================

        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:

                result = {
                    "error": (
                        "The AI generated invalid "
                        "tool arguments."
                    )
                }

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    }
                )

                continue


            # =================================================
            # TOOL 1 — SEARCH RESUME
            # =================================================

            if function_name == "search_resume":

                result = search_resume_tool(
                    arguments.get(
                        "query",
                        ""
                    )
                )


            # =================================================
            # TOOL 2 — ANALYZE JOB DESCRIPTION
            # =================================================

            elif function_name == "analyze_job_description":

                result = analyze_job_description(
                    arguments.get(
                        "job_description",
                        ""
                    )
                )


            # =================================================
            # TOOL 3 — MATCH SKILLS
            # =================================================

            elif function_name == "match_skills":

                result = match_skills(
                    arguments.get(
                        "resume_information",
                        ""
                    ),
                    arguments.get(
                        "job_description",
                        ""
                    )
                )


            # =================================================
            # TOOL 4 — GENERATE INTERVIEW
            # =================================================

            elif function_name == "generate_interview":

                result = generate_interview_tool(
                    arguments.get(
                        "resume_information",
                        ""
                    ),
                    arguments.get(
                        "job_description",
                        ""
                    )
                )


            # =================================================
            # TOOL 5 — START INTERVIEW
            # =================================================

            elif function_name == "start_interview":

                result = start_interview_tool(
                    arguments.get(
                        "resume_information",
                        ""
                    ),
                    arguments.get(
                        "job_description",
                        ""
                    )
                )


            # =================================================
            # TOOL 6 — EVALUATE ANSWER
            # =================================================

            elif function_name == "evaluate_answer":

                result = evaluate_answer_tool(
                    arguments.get(
                        "question",
                        ""
                    ),
                    arguments.get(
                        "answer",
                        ""
                    )
                )


            # =================================================
            # TOOL 7 — GENERATE NEXT QUESTION
            # =================================================

            elif function_name == "generate_next_question":

                result = generate_next_question_tool(
                    arguments.get(
                        "resume_information",
                        ""
                    ),
                    arguments.get(
                        "job_description",
                        ""
                    ),
                    arguments.get(
                        "previous_question",
                        ""
                    ),
                    arguments.get(
                        "previous_answer",
                        ""
                    )
                )


            # =================================================
            # UNKNOWN TOOL
            # =================================================

            else:

                result = {
                    "error": (
                        f"Unknown tool: {function_name}"
                    )
                }


            # =================================================
            # CONVERT RESULT TO STRING
            # =================================================

            if isinstance(result, str):

                tool_result = result

            else:

                tool_result = json.dumps(
                    result,
                    ensure_ascii=False
                )


            # =================================================
            # SEND TOOL RESULT BACK TO LLM
            # =================================================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )


    # =====================================================
    # FALLBACK
    # =====================================================

    return (
        "I couldn't complete the request. "
        "Please try asking the question again."
    )