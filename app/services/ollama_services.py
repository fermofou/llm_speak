import requests

def chat_with_model(message: str):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "qwen2.5:7b",
            "messages": [
                {"role": "user", "content": message}
            ],
            "stream": False
        }
    )
    return response.json()