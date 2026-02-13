"""
Request and response schemas for the chat API.
All data is validated through Pydantic.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    """Request to send a message to the LLM"""
    message: str = Field(..., min_length=1, max_length=5000)
    history: Optional[List[Dict[str, str]]] = Field(None, description="Previous messages")


class ToolResult(BaseModel):
    """Result from a tool execution"""
    tool: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    success: bool
    response: Optional[str] = None
    tool_results: Optional[List[ToolResult]] = None
    error: Optional[str] = None
    available_tools: Optional[List[str]] = None


class SpeakRequest(BaseModel):
    """Request to send voice to the LLM"""
    duration: int = Field(default=5, ge=1, le=60)
    language: Optional[str] = Field(default="en")


class SpeakResponse(BaseModel):
    """Response from speak endpoint"""
    success: bool
    transcribed_text: Optional[str] = None
    language: Optional[str] = None
    response: Optional[str] = None
    tool_results: Optional[List[ToolResult]] = None
    error: Optional[str] = None


class ToolListResponse(BaseModel):
    """Response with available tools"""
    available_tools: List[str]
    count: int
