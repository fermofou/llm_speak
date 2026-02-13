import requests
from app.tools.tool_registry import execute_tool

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:7b"  # or your model


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
    }
]


def process_message(message: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": message}
            ],
            "tools": TOOLS,
            "stream": False
        }
    )

    data = response.json()

    # Check if tool call
    if "tool_calls" in data["message"]:

        tool_call = data["message"]["tool_calls"][0]
        tool_name = tool_call["name"]
        tool_args = tool_call["arguments"]

        result = execute_tool(tool_name, tool_args)

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
