from fastapi import FastAPI
from pydantic import BaseModel
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:7b"

app = FastAPI()

class ChatRequest(BaseModel):
    message: str


def call_ollama(user_message: str):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful bilingual assistant (English/Spanish)."},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["message"]["content"]


@app.post("/chat")
def chat(req: ChatRequest):
    reply = call_ollama(req.message)
    return {"response": reply}
