"""
Centralized configuration using Pydantic Settings.
Prevents os.getenv() scattered everywhere.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from .env"""
    
    # Ollama Configuration
    ollama_url: str = "http://localhost:11434/api/chat"
    ollama_model: str = "qwen2.5:7b"
    ollama_timeout: int = 30
    
    # Spotify Configuration (Optional)
    spotify_client_id: Optional[str] = None
    spotify_client_secret: Optional[str] = None
    spotify_redirect_uri: Optional[str] = None
    
    # Weather Configuration (Optional)
    openweather_api_key: Optional[str] = None
    
    # Speech Configuration
    speech_language: str = "en"
    speech_model: str = "base"
    
    # Security & Logging
    log_level: str = "INFO"
    log_tool_execution: bool = True
    enable_tool_auditing: bool = True
    
    # Rate Limiting
    max_requests_per_minute: int = 30
    max_tool_calls_per_minute: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
