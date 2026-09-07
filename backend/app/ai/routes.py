from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.agent import run_agent


router = APIRouter(
    prefix="/api/ai",
    tags=["AI Helpdesk"],
)


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        return {
            "success": False,
            "message": "Please describe your IT problem.",
        }

    try:
        result = run_agent(request.message)

        return {
            "success": True,
            "data": result,
        }

    except Exception as error:
        return {
            "success": False,
            "message": "Unable to process the helpdesk request.",
            "error": str(error),
        }
