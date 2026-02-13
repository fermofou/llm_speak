from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_service import process_message

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat(req: ChatRequest):
    return process_message(req.message)
