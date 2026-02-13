"""
Tool definition and validation schemas.
These define the EXACT tools available to the LLM.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from enum import Enum


class ToolName(str, Enum):
    """Whitelist of allowed tools. ONLY these can be called."""
    
    # Spotify
    PLAY_SONG = "play_song"
    PAUSE_PLAYBACK = "pause_playback"
    RESUME_PLAYBACK = "resume_playback"
    NEXT_TRACK = "next_track"
    PREVIOUS_TRACK = "previous_track"
    GET_CURRENT_TRACK = "get_current_track"
    
    # Weather
    CHECK_WEATHER = "check_weather"
    GET_FORECAST = "get_forecast"
    
    # Wikipedia
    SEARCH_WIKI = "search_wiki"
    GET_WIKI_SUMMARY = "get_wiki_summary"


# Tool argument schemas for validation
class PlaySongArgs(BaseModel):
    """Arguments for play_song tool"""
    song: str = Field(..., min_length=1, max_length=500)
    
    @validator("song")
    def song_must_not_have_urls(cls, v):
        """Prevent URL injection"""
        if "://" in v or v.startswith("http"):
            raise ValueError("Song name cannot contain URLs")
        return v


class CheckWeatherArgs(BaseModel):
    """Arguments for check_weather tool"""
    city: str = Field(..., min_length=1, max_length=100)
    
    @validator("city")
    def city_must_not_have_special_chars(cls, v):
        """Prevent injection attacks"""
        import re
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", v):
            raise ValueError("City name contains invalid characters")
        return v


class GetForecastArgs(BaseModel):
    """Arguments for get_forecast tool"""
    city: str = Field(..., min_length=1, max_length=100)
    days: int = Field(default=5, ge=1, le=14)
    
    @validator("city")
    def city_must_not_have_special_chars(cls, v):
        """Prevent injection attacks"""
        import re
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", v):
            raise ValueError("City name contains invalid characters")
        return v


class SearchWikiArgs(BaseModel):
    """Arguments for search_wiki tool"""
    query: str = Field(..., min_length=1, max_length=500)
    sentences: int = Field(default=3, ge=1, le=10)
    
    @validator("query")
    def query_must_not_have_urls(cls, v):
        """Prevent URL injection"""
        if "://" in v or v.startswith("http"):
            raise ValueError("Query cannot contain URLs")
        return v


class GetWikiSummaryArgs(BaseModel):
    """Arguments for get_wiki_summary tool"""
    page_title: str = Field(..., min_length=1, max_length=500)
    
    @validator("page_title")
    def page_title_must_not_have_urls(cls, v):
        """Prevent URL injection"""
        if "://" in v or v.startswith("http"):
            raise ValueError("Page title cannot contain URLs")
        return v


# Map tool names to their argument schemas
TOOL_SCHEMAS: Dict[ToolName, BaseModel] = {
    ToolName.PLAY_SONG: PlaySongArgs,
    ToolName.CHECK_WEATHER: CheckWeatherArgs,
    ToolName.GET_FORECAST: GetForecastArgs,
    ToolName.SEARCH_WIKI: SearchWikiArgs,
    ToolName.GET_WIKI_SUMMARY: GetWikiSummaryArgs,
}

# Tools that don't take arguments
NO_ARG_TOOLS = {
    ToolName.PAUSE_PLAYBACK,
    ToolName.RESUME_PLAYBACK,
    ToolName.NEXT_TRACK,
    ToolName.PREVIOUS_TRACK,
    ToolName.GET_CURRENT_TRACK,
}


def validate_tool_call(tool_name: str, tool_args: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate a tool call request from the LLM.
    
    Returns:
        (is_valid, error_message)
    """
    # 1. Check tool exists in whitelist
    try:
        tool = ToolName(tool_name)
    except ValueError:
        return False, f"Tool '{tool_name}' not in whitelist. Available: {[t.value for t in ToolName]}"
    
    # 2. Check no-arg tools
    if tool in NO_ARG_TOOLS:
        if tool_args:
            return False, f"Tool '{tool_name}' does not accept arguments"
        return True, ""
    
    # 3. Validate arguments
    if tool not in TOOL_SCHEMAS:
        return False, f"No schema defined for tool '{tool_name}'"
    
    try:
        schema = TOOL_SCHEMAS[tool]
        schema(**tool_args)  # This will raise if invalid
        return True, ""
    except ValueError as e:
        return False, f"Invalid arguments for '{tool_name}': {str(e)}"
