from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.assistant import generate_helpdesk_response


router = APIRouter(prefix="/api/ai", tags=["AI Helpdesk"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        return {
            "success": False,
            "message": "Please describe your IT problem.",
        }

    result = generate_helpdesk_response(request.message)

    return {
        "success": True,
        "data": result,
    }
