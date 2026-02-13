"""
Chat router - HTTP endpoints for messaging and voice interaction.
All requests validated, all tool calls logged.
"""

from fastapi import APIRouter, HTTPException
from app.services.chat_service import process_message
from app.services.speech_service import speech_to_text
from app.tools.tool_registry import AVAILABLE_TOOLS
from app.schemas.responses import ChatRequest, ChatResponse, SpeakRequest, SpeakResponse, ToolListResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a text message to the LLM and get a response.
    The LLM may call tools to answer your question.
    """
    result = process_message(req.message, req.history)
    return result


@router.get("/tools", response_model=ToolListResponse)
async def list_tools():
    """
    List all available tools that the LLM can use.
    These are the ONLY tools the model can call.
    """
    return ToolListResponse(
        available_tools=list(AVAILABLE_TOOLS.keys()),
        count=len(AVAILABLE_TOOLS)
    )


@router.post("/speak", response_model=SpeakResponse)
async def speak_to_chat(duration: int = 5, language: str = "en"):
    """
    Record audio, transcribe it, and send to LLM.
    
    The system will:
    1. Record your voice for the specified duration
    2. Convert speech to text using Whisper
    3. Send the text to the LLM
    4. Return the response
    
    Args:
        duration: Duration of recording in seconds (1-60)
        language: Language code (e.g., 'en' for English)
    """
    try:
        # Transcribe speech
        transcription = speech_to_text(duration, language)
        
        if not transcription.get("success"):
            raise HTTPException(
                status_code=400,
                detail=transcription.get("error", "Speech recognition failed")
            )
        
        user_text = transcription.get("text")
        
        # Process with LLM
        result = process_message(user_text)
        
        return SpeakResponse(
            success=True,
            transcribed_text=user_text,
            language=transcription.get("language"),
            response=result.get("response"),
            tool_results=result.get("tool_results")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
