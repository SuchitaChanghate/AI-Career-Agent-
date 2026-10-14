from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.agent import run_agent


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


# =========================================================
# CHAT MESSAGE
# =========================================================

class ChatMessage(BaseModel):
    role: str
    content: str


# =========================================================
# CHAT REQUEST
# =========================================================

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []


# =========================================================
# CHAT ENDPOINT
# =========================================================

@router.post("/")
def chat(request: ChatRequest):

    response = run_agent(
        user_message=request.message,
        chat_history=[
            {
                "role": message.role,
                "content": message.content
            }
            for message in request.history
        ]
    )

    return {
        "response": response
    }