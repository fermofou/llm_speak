import requests
from app.tools.tool_registry import execute_tool, AVAILABLE_TOOLS
from app.core.config import settings

OLLAMA_URL = settings.ollama_url
MODEL_NAME = settings.ollama_model

# Define tools for Ollama
TOOLS = [
    {
        "name": "play_song",
        "description": "Play a song on Spotify",
        "parameters": {
            "type": "object",
            "properties": {
                "song": {
                    "type": "string",
                    "description": "Song name and optionally artist"
                }
            },
            "required": ["song"]
        }
    },
    {
        "name": "check_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_forecast",
        "description": "Get weather forecast for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days forecast (default: 5)"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "search_wiki",
        "description": "Search Wikipedia for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "sentences": {
                    "type": "integer",
                    "description": "Number of sentences to return (default: 3)"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_wiki_summary",
        "description": "Get a summary of a Wikipedia page",
        "parameters": {
            "type": "object",
            "properties": {
                "page_title": {
                    "type": "string",
                    "description": "Wikipedia page title"
                }
            },
            "required": ["page_title"]
        }
    }
]


def process_message(message: str, history: list = None) -> dict:
    """
    Process a user message with Ollama and execute tools if needed.
    
    Args:
        message: User message
        history: Chat history (optional)
        
    Returns:
        Dictionary with response and tool results
    """
    if history is None:
        history = []
    
    # Add user message to history
    messages = history + [{"role": "user", "content": message}]
    
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "tools": TOOLS,
                "stream": False
            },
            timeout=settings.ollama_timeout
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Cannot connect to Ollama service. Make sure Ollama is running on localhost:11434"
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "Ollama service timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Ollama service error: {str(e)}"
        }
    
    data = response.json()
    
    # Extract response
    if "message" not in data:
        return {
            "success": False,
            "error": "Invalid response from Ollama"
        }
    
    message_data = data["message"]
    response_text = message_data.get("content", "")
    
    # Check if tool call is needed
    tool_results = []
    if "tool_calls" in message_data and message_data["tool_calls"]:
        for tool_call in message_data["tool_calls"]:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("arguments", {})
            
            result = execute_tool(tool_name, tool_args)
            tool_results.append({
                "tool": tool_name,
                "result": result
            })
    
    return {
        "success": True,
        "response": response_text,
        "tool_results": tool_results if tool_results else None,
        "available_tools": list(AVAILABLE_TOOLS.keys())
    }

        return {
            "type": "tool_executed",
            "tool": tool_name,
            "result": result
        }

    # Otherwise normal LLM answer
    return {
        "type": "chat",
        "response": data["message"]["content"]
    }
