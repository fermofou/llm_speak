"""
Tool execution registry with security validation.
This is the ONLY place where tools are executed.
All calls go through validation first.
"""

import time
from app.tools.spotify_tools import (
    play_song,
    pause_playback,
    resume_playback,
    next_track,
    previous_track,
    get_current_track,
)
from app.tools.weather_tools import check_weather, get_forecast
from app.tools.wikipedia_tools import search_wiki, get_wiki_summary

from app.core.security import validate_tool_call, ToolName, NO_ARG_TOOLS
from app.core.logging import ToolExecutionAudit, log_security_event

AVAILABLE_TOOLS = {
    # Spotify tools
    "play_song": play_song,
    "pause_playback": pause_playback,
    "resume_playback": resume_playback,
    "next_track": next_track,
    "previous_track": previous_track,
    "get_current_track": get_current_track,
    # Weather tools
    "check_weather": check_weather,
    "get_forecast": get_forecast,
    # Wikipedia tools
    "search_wiki": search_wiki,
    "get_wiki_summary": get_wiki_summary,
}


def execute_tool(tool_name: str, tool_args: dict = None) -> dict:
    """
    Execute a tool with full security validation.
    
    SECURITY GUARANTEES:
    1. Tool must be in whitelist
    2. Arguments must pass schema validation
    3. All executions are logged
    4. No arbitrary code execution
    
    Args:
        tool_name: The name of the tool to execute
        tool_args: Dictionary of arguments for the tool
        
    Returns:
        Dictionary with the result of tool execution
    """
    
    if tool_args is None:
        tool_args = {}
    
    start_time = time.time()
    
    # STEP 1: Validate tool call against security rules
    is_valid, error_msg = validate_tool_call(tool_name, tool_args)
    
    if not is_valid:
        # Tool rejected - log security event
        log_security_event(
            event_type="tool_rejected",
            description=f"Tool call rejected: {error_msg}",
            severity="WARNING"
        )
        ToolExecutionAudit.log_tool_rejection(tool_name, error_msg, tool_args)
        
        return {
            "success": False,
            "error": error_msg,
            "tool": tool_name
        }
    
    # STEP 2: Log the tool call attempt
    ToolExecutionAudit.log_tool_call(tool_name, tool_args)
    
    # STEP 3: Execute the tool
    try:
        # Get the tool function
        if tool_name not in AVAILABLE_TOOLS:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(AVAILABLE_TOOLS.keys())
            }
        
        tool_func = AVAILABLE_TOOLS[tool_name]
        
        # Execute with arguments if needed
        if tool_name in [t.value for t in NO_ARG_TOOLS]:
            result = tool_func()
        else:
            result = tool_func(**tool_args)
        
        # STEP 4: Log successful execution
        execution_time = (time.time() - start_time) * 1000
        ToolExecutionAudit.log_tool_result(
            tool_name,
            success=True,
            result=result,
            execution_time_ms=execution_time
        )
        
        return {
            "success": True,
            "tool": tool_name,
            "result": result
        }
        
    except Exception as e:
        # STEP 5: Log execution error
        execution_time = (time.time() - start_time) * 1000
        error_str = str(e)
        
        log_security_event(
            event_type="tool_execution_error",
            description=f"Tool '{tool_name}' failed: {error_str}",
            severity="ERROR"
        )
        
        ToolExecutionAudit.log_tool_result(
            tool_name,
            success=False,
            result=None,
            error=error_str,
            execution_time_ms=execution_time
        )
        
        return {
            "success": False,
            "tool": tool_name,
            "error": f"Tool execution failed: {error_str}"
        }
