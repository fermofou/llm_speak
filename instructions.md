Let’s define each folder **clearly and practically**, not academically.

You’re building an AI assistant backend. So structure matters.

---

# 🧠 The Philosophy

Think in layers:

```
API Layer (routers)
Business Logic (services)
Capabilities (tools)
Configuration (core)
Data Contracts (schemas)
```

Each has a different responsibility.

---

# 📁 core/

### Purpose:

Global configuration & shared infrastructure.

Put here:

- config.py (loads .env)
- settings
- constants
- logging setup
- security rules
- dependency injection helpers

Example:

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
```

This prevents `os.getenv()` scattered everywhere.

---

# 📁 routers/

### Purpose:

HTTP layer only.

These define your API endpoints.

They:

- Receive requests
- Validate input
- Call services
- Return responses

They DO NOT:

- Call external APIs directly
- Contain business logic
- Contain model logic

Example:

```python
@router.post("/chat")
def chat(request: ChatRequest):
    return chat_service.process_message(request.message)
```

Think: controllers.

---

# 📁 schemas/

### Purpose:

Define request/response shapes using Pydantic.

This keeps:

- Type safety
- Validation
- Clean API docs
- Structured tool calling

Example:

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
```

This prevents random dicts everywhere.

---

# 📁 services/

### Purpose:

Business logic + external engines.

This is the brain of your backend.

Put here:

- Ollama interaction
- Spotify OAuth logic
- Whisper transcription
- TTS execution
- Token refresh logic

Services:

- Can call tools
- Can call APIs
- Should not define HTTP routes

Example:

```python
def chat_with_model(message: str):
    ...
```

Think: “how the system works”.

---

# 📁 tools/

### Purpose:

LLM-allowed capabilities.

These are controlled, safe, atomic actions.

Examples:

- get_weather()
- search_wikipedia()
- play_spotify()
- pause_spotify()

These are the only things your model should be allowed to trigger.

Important difference:

Service = infrastructure
Tool = capability exposed to LLM

---

# 🔥 Critical Distinction

Many beginners mix services and tools.

Here’s the difference:

| Services       | Tools                |
| -------------- | -------------------- |
| System logic   | AI-exposed functions |
| OAuth handling | play_song()          |
| Token refresh  | search_wikipedia()   |
| Model calls    | pause_spotify()      |

Services are internal.
Tools are “buttons” the AI can press.

---

# 🧠 Why This Matters For You

You said:

> avoid code execution or security problems

This structure allows:

- Strict tool whitelist
- No arbitrary execution
- Clear boundaries
- Easy auditing

---

# 🏗 Real Example Flow

User says:
“Play Daft Punk”

1. Router receives /chat
2. Service calls Ollama
3. Ollama returns:

   ```
   {
     "tool": "play_spotify",
     "args": {"song": "Daft Punk"}
   }
   ```

4. Service validates tool exists
5. Tool executes Spotify API call
6. Result returned to model
7. Model formats final answer

Clean.
Controlled.
Safe.

---

# 🚀 Why This Structure Scales

Later you will add:

- Memory
- Permissions
- User accounts
- Logging
- Rate limiting
- Multi-device voice
- Tool usage tracking

Without separation → impossible.

With separation → easy.

---

# 📌 Short Summary

core → configuration
routers → HTTP endpoints
schemas → request/response models
services → logic & external engines
tools → LLM capabilities

---
