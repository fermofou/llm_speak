# LLM Speech Assistant

A FastAPI-based intelligent voice-activated assistant that understands speech, processes queries with Ollama LLM, and can control Spotify, check weather, search Wikipedia, and more.

## Features

- 🎤 **Speech Recognition**: Convert speech to text using OpenAI's Whisper model
- 🤖 **LLM Processing**: Use Ollama with local models for intelligent responses
- 🎵 **Spotify Integration**: Control music playback
- 🌤️ **Weather Information**: Check current weather and forecasts
- 📚 **Wikipedia Search**: Search and retrieve information from Wikipedia
- 🛠️ **Tool Management**: Extensible tool system for adding more capabilities

## Prerequisites

### Required

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running locally
- An Ollama model (e.g., `qwen2.5:7b`)

### Optional

- Spotify API credentials (for music control)
- OpenWeatherMap API key (for weather)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/llm_speak.git
cd llm_speak
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Start Ollama** (if not running)

```bash
ollama run qwen2.5:7b
# Or pull the model first: ollama pull qwen2.5:7b
```

6. **Run the application**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Chat Endpoints

#### Send Text Message

```bash
POST /chat/message
{
  "message": "What's the weather in New York?",
  "history": []
}
```

#### List Available Tools

```bash
GET /chat/tools
```

#### Speech to Chat (Record and Process)

```bash
POST /chat/speak?duration=5&language=en
```

### Health Check

```bash
GET /health
```

## Quick Start

### Text Chat Example

```python
import requests

response = requests.post(
    "http://localhost:8000/chat/message",
    json={
        "message": "Tell me about Python",
        "history": []
    }
)
print(response.json())
```

### Voice Chat Example

```python
import requests

# Record voice for 5 seconds and process
response = requests.post(
    "http://localhost:8000/chat/speak?duration=5&language=en"
)
print(response.json())
```

## Project Structure

```
app/
├── main.py                 # FastAPI application
├── routers/
│   ├── chat_router.py     # Chat endpoints
│   └── spotify_router.py  # Spotify endpoints
├── services/
│   ├── chat_service.py    # LLM processing
│   ├── ollama_services.py # Ollama integration
│   ├── spotify_service.py # Spotify API
│   ├── weather_service.py # Weather service
│   ├── wikipedia_service.py # Wikipedia service
│   └── speech_service.py  # Speech recognition
├── tools/
│   ├── tool_registry.py   # Tool management
│   ├── spotify_tools.py   # Spotify wrappers
│   ├── weather_tools.py   # Weather wrappers
│   └── wikipedia_tools.py # Wikipedia wrappers
└── schemas/
    └── chat_message.py    # Data models
```

## Environment Configuration

Create a `.env` file:

```
OLLAMA_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=qwen2.5:7b

SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/spotify/callback

OPENWEATHER_API_KEY=your_api_key
SPEECH_LANGUAGE=en
```

## Troubleshooting

### "Cannot connect to Ollama service"

- Make sure Ollama is running: `ollama serve`
- Check at `http://localhost:11434`

### "Whisper not installed"

- Install: `pip install openai-whisper`

### "Audio recording failed"

- Install: `pip install sounddevice soundfile`

### Import errors

- Ensure in virtual environment
- Run: `pip install -r requirements.txt`

## Future Enhancements

- [ ] Text-to-Speech responses
- [ ] Multi-turn conversation context
- [ ] Web UI frontend
- [ ] Database for chat history
- [ ] More tool integrations
- [ ] Docker support

## License

MIT License - see LICENSE file for details.
