# 🧭 Quick Reference: Security & Structure

## 📍 Where Everything Is

### Configuration & Secrets

```
app/core/config.py
  - All settings loaded from .env
  - Centralized, type-safe
  - Use: from app.core.config import settings
```

### Tool Safety

```
app/core/security.py
  - Tool whitelist (ToolName enum)
  - Argument validators (Pydantic)
  - validation function

Whitelist:
  - play_song
  - check_weather
  - search_wiki
  - (+ 7 more, only these can be called)
```

### Execution & Logging

```
app/core/logging.py
  - ToolExecutionAudit class
  - Logs all tool calls
  - Logs all results
  - Logs security events
```

### Tool Execution (Hardened)

```
app/tools/tool_registry.py
  - execute_tool() function
  - Validates tool call
  - Validates arguments
  - Logs execution
  - Only runs whitelisted tools
```

---

## 🔐 Security Flow

```
Request arrives
  ↓
[Router] - Validate with Pydantic schema
  ↓
[Service] - Call Ollama
  ↓
[Ollama] - Returns {"tool": "X", "args": {...}}
  ↓
[Tool Registry] - VALIDATE
  ├─ Is tool whitelisted?
  ├─ Are arguments valid?
  ├─ Log the call
  ↓
[Execute Tool] - Only if validation passed
  ├─ Call external API
  ├─ Log result
  ↓
[Return Response] - Validated response
```

---

## 🛠️ Adding a New Tool Safely

### 1. Add to Whitelist

**File:** `app/core/security.py`

```python
class ToolName(str, Enum):
    # ... existing tools ...
    MY_NEW_TOOL = "my_new_tool"
```

### 2. Add Argument Schema

**File:** `app/core/security.py`

```python
class MyNewToolArgs(BaseModel):
    param1: str = Field(..., min_length=1, max_length=100)
    param2: int = Field(default=5, ge=1, le=10)

    @validator("param1")
    def validate_param1(cls, v):
        # Your validation
        if not v.isalnum():
            raise ValueError("Only alphanumeric allowed")
        return v
```

### 3. Register Schema

**File:** `app/core/security.py`

```python
TOOL_SCHEMAS: Dict[ToolName, BaseModel] = {
    # ... existing ...
    ToolName.MY_NEW_TOOL: MyNewToolArgs,
}
```

### 4. Implement Tool

**File:** `app/tools/my_tools.py`

```python
def my_new_tool(param1: str, param2: int = 5) -> dict:
    # Your logic here
    return {"success": True, "result": "..."}
```

### 5. Register in Registry

**File:** `app/tools/tool_registry.py`

```python
from app.tools.my_tools import my_new_tool

AVAILABLE_TOOLS = {
    # ... existing ...
    "my_new_tool": my_new_tool,
}
```

**That's it! Your tool is now:**

- ✅ Whitelisted
- ✅ Argument-validated
- ✅ Fully audited
- ✅ Safe to use

---

## 🚨 What Gets Blocked

```python
# ❌ Tool not in whitelist
Tool: "exec_system_command"  → REJECTED

# ❌ URL injection
Tool: "check_weather"
Args: {"city": "http://evil.com"}  → REJECTED

# ❌ Special characters
Tool: "check_weather"
Args: {"city": "New York<script>"}  → REJECTED

# ❌ Length exceeded
Tool: "check_weather"
Args: {"city": "A" * 1000}  → REJECTED
```

---

## 📊 Audit Trail

Every tool execution creates logs:

**Tool Call:**

```json
{
  "timestamp": "2026-02-13T10:30:45.123Z",
  "event": "tool_call",
  "tool": "check_weather",
  "args": { "city": "Paris" }
}
```

**Tool Result:**

```json
{
  "timestamp": "2026-02-13T10:30:46.456Z",
  "event": "tool_result",
  "tool": "check_weather",
  "success": true,
  "execution_time_ms": 1233
}
```

**Tool Rejected:**

```json
{
  "timestamp": "2026-02-13T10:30:47.789Z",
  "event": "tool_rejected",
  "tool": "check_weather",
  "reason": "Invalid arguments for 'check_weather': City name contains invalid characters",
  "args": { "city": "New York<script>alert(1)</script>" }
}
```

---

## 🔧 Common Operations

### Check Configuration

```python
from app.core.config import settings

print(settings.ollama_url)
print(settings.ollama_model)
print(settings.log_tool_execution)
```

### Validate a Tool Call

```python
from app.core.security import validate_tool_call

is_valid, error_msg = validate_tool_call(
    "check_weather",
    {"city": "Paris"}
)

if not is_valid:
    print(f"Invalid: {error_msg}")
```

### Execute a Tool

```python
from app.tools.tool_registry import execute_tool

result = execute_tool("check_weather", {"city": "Paris"})
print(result)  # {"success": True, "tool": "check_weather", "result": {...}}
```

### List Available Tools

```python
from app.tools.tool_registry import AVAILABLE_TOOLS

for tool_name in AVAILABLE_TOOLS.keys():
    print(f"- {tool_name}")
```

---

## 🎓 Design Principles

### From `instructions.md`

| Layer         | Purpose          | Rules                          |
| ------------- | ---------------- | ------------------------------ |
| **routers/**  | HTTP endpoints   | Only validate & call services  |
| **services/** | Business logic   | Call tools, call APIs, no HTTP |
| **tools/**    | LLM capabilities | Atomic, safe, whitelisted only |
| **core/**     | Configuration    | Settings, security, logging    |
| **schemas/**  | Data contracts   | Pydantic models for validation |

**Tools are the ONLY things the LLM can execute.**
**Everything else is internal infrastructure.**

---

## 📋 Production Checklist

- [ ] Read `SECURITY.md`
- [ ] Review `app/core/security.py`
- [ ] Run `python test_structure.py` ✅
- [ ] Check `.env` has all required keys
- [ ] Start Ollama: `ollama serve`
- [ ] Start app: `uvicorn app.main:app`
- [ ] Test via API: `POST /chat/message`
- [ ] Monitor logs for security events

---

## 🆘 Troubleshooting

### Import Error

```
ImportError: cannot import name 'execute_tool'
```

**Fix:** Run `pip install -r requirements.txt`

### "Ollama not found"

```
error: Cannot connect to Ollama service
```

**Fix:** Run `ollama serve` in another terminal

### "Whisper not installed"

```
error: Whisper is not installed
```

**Fix:** Run `pip install openai-whisper`

### Validation errors

```
Invalid arguments for 'check_weather': City name contains invalid characters
```

**Fix:** Check tool argument validators in `app/core/security.py`

---

## 📞 Support

- 📖 Read `SECURITY.md` for detailed architecture
- 📖 Read `IMPROVEMENTS.md` for what changed
- 📖 Read `instructions.md` for design philosophy
- 🧪 Run `test_structure.py` to validate setup
- 🔍 Check logs for security events

---

**Stay secure. Stay audited. Stay safe.** 🔒
