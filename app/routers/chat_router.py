from fastapi import APIRouter
from app.services.ollama_service import chat_with_model

router = APIRouter()

@router.post("/chat")
def chat(message: str):
    return chat_with_model(message)
