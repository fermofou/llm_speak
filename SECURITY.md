# 🔐 Security Architecture

This document explains the security guarantees built into the LLM assistant.

---

## ✅ Security Guarantees

### 1. **Tool Whitelist (No Arbitrary Execution)**

All tools the LLM can call are explicitly whitelisted in `app/core/security.py`:

```python
class ToolName(str, Enum):
    PLAY_SONG = "play_song"
    CHECK_WEATHER = "check_weather"
    SEARCH_WIKI = "search_wiki"
    # ... only these can be called
```

**If the LLM tries to call any other tool, the request is REJECTED.**

### 2. **Argument Validation (No Injection)**

Every tool has strict Pydantic validation:

```python
class CheckWeatherArgs(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)

    @validator("city")
    def city_must_not_have_special_chars(cls, v):
        import re
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", v):
            raise ValueError("City name contains invalid characters")
        return v
```

**The LLM cannot inject URLs, SQL, or malicious code through tool arguments.**

### 3. **Input Sanitization**

Specific checks prevent common attacks:

- **URL Prevention**: Any argument with `://` is rejected
- **Special Characters**: Only safe characters allowed
- **Length Limits**: Arguments bounded (min/max length)

### 4. **Execution Logging & Auditing**

Every tool call is logged:

```python
ToolExecutionAudit.log_tool_call(tool_name, tool_args)
ToolExecutionAudit.log_tool_result(tool_name, success, result)
```

**You can audit exactly:**

- What tool was called
- When it was called
- What arguments were passed
- What happened (success/error)
- How long it took

Logs are written to files and can be monitored.

### 5. **Centralized Configuration**

All secrets and settings are in ONE place: `app/core/config.py`

```python
class Settings(BaseSettings):
    ollama_url: str = "http://localhost:11434/api/chat"
    spotify_client_id: Optional[str] = None
    openweather_api_key: Optional[str] = None
```

**No scattered `.env` loading. No secrets hardcoded in services.**

### 6. **Strict Type Validation**

Request bodies are validated with Pydantic:

```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    history: Optional[List[Dict[str, str]]] = None
```

**Bad requests are rejected before they reach business logic.**

---

## 🏗️ How Security Works (Flow)

```
User Request
    ↓
[FastAPI Router] - Validate request with Pydantic
    ↓
[Service] - Process message with Ollama
    ↓
[LLM] - Returns tool call (if needed)
    ↓
[Tool Registry] - VALIDATE tool call
    ├─ Is tool in whitelist? NO → REJECT
    ├─ Are arguments valid? NO → REJECT
    ├─ Log the call → Audit trail created
    ↓
[Tool Execution] - Execute only if validation passed
    ├─ Log result
    ├─ Return to LLM
    ↓
[Response] - Validated response sent to user
```

---

## 🚨 What This PREVENTS

### ❌ Remote Code Execution

LLM cannot execute arbitrary code. Only whitelisted tools allowed.

### ❌ SQL Injection

All tool arguments are validated and sanitized.

### ❌ Command Injection

Tool arguments have restricted character sets.

### ❌ Secret Leakage

Configuration centralized. Easy to audit for sensitive data exposure.

### ❌ Unauthorized Tool Usage

Every tool call is logged. You can monitor and alert on suspicious activity.

### ❌ Argument Manipulation

Pydantic validators prevent malicious input.

---

## 📋 Audit Trail Example

```json
{
  "timestamp": "2026-02-13T10:30:45.123Z",
  "event": "tool_call",
  "tool": "check_weather",
  "args": { "city": "New York" },
  "user_message": "What's the weather?"
}
```

```json
{
  "timestamp": "2026-02-13T10:30:46.456Z",
  "event": "tool_result",
  "tool": "check_weather",
  "success": true,
  "execution_time_ms": 1233
}
```

---

## 🔧 Adding New Tools Safely

To add a new tool:

1. **Define in whitelist** (`app/core/security.py`):

```python
class ToolName(str, Enum):
    NEW_TOOL = "new_tool"
```

2. **Create argument schema** (`app/core/security.py`):

```python
class NewToolArgs(BaseModel):
    param: str = Field(..., min_length=1, max_length=100)

    @validator("param")
    def validate_param(cls, v):
        # Your validation here
        return v
```

3. **Register schema** (`app/core/security.py`):

```python
TOOL_SCHEMAS: Dict[ToolName, BaseModel] = {
    ToolName.NEW_TOOL: NewToolArgs,
}
```

4. **Implement tool** (`app/tools/new_tools.py`)

5. **Register in registry** (`app/tools/tool_registry.py`):

```python
from app.tools.new_tools import new_tool

AVAILABLE_TOOLS = {
    "new_tool": new_tool,
}
```

**Your tool is now audited and sandboxed.**

---

## 📊 Configuration: Security Settings

In `.env`:

```
# Enable execution logging (ALWAYS on in production)
LOG_TOOL_EXECUTION=true

# Enable tool auditing (ALWAYS on in production)
ENABLE_TOOL_AUDITING=true

# Rate limiting (adjust based on needs)
MAX_REQUESTS_PER_MINUTE=30
MAX_TOOL_CALLS_PER_MINUTE=10
```

---

## 🛑 Rate Limiting (Future Enhancement)

Currently configured, ready to implement:

```python
max_requests_per_minute: int = 30
max_tool_calls_per_minute: int = 10
```

This prevents DOS attacks and LLM hallucination loops.

---

## 🔒 Best Practices

1. **Keep logs**: Never delete audit logs
2. **Monitor tools**: Alert on suspicious tool calls
3. **Validate secrets**: Ensure all API keys are in `.env`
4. **Test tools**: Test new tools locally before deployment
5. **Review schemas**: Add validators for every tool argument
6. **Update regularly**: Keep dependencies updated

---

## ⚠️ Limitations & Future Work

### Current Scope

- ✅ Prevents arbitrary code execution
- ✅ Validates all tool arguments
- ✅ Full audit trail
- ✅ Whitelisted tools only

### Future Enhancements

- [ ] Rate limiting middleware
- [ ] User authentication/authorization
- [ ] Tool usage quotas per user
- [ ] Secret rotation
- [ ] Encrypted audit logs
- [ ] Real-time alert system
- [ ] Tool usage analytics

---

## 🚀 You Are Safe

The LLM cannot:

- ❌ Execute arbitrary code
- ❌ Inject malicious input
- ❌ Call tools outside the whitelist
- ❌ Do anything without it being logged

**Everything is auditable. Everything is controlled.**
