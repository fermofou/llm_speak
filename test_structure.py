"""
Quick test to verify project structure and imports work.
Run this before deploying.
"""

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    
    # Core
    from app.core.config import settings
    from app.core.security import validate_tool_call, ToolName
    from app.core.logging import ToolExecutionAudit
    
    # Services
    from app.services.chat_service import process_message
    from app.services.weather_service import get_weather
    from app.services.speech_service import speech_to_text
    
    # Tools
    from app.tools.tool_registry import execute_tool, AVAILABLE_TOOLS
    from app.tools.spotify_tools import play_song
    from app.tools.weather_tools import check_weather
    from app.tools.wikipedia_tools import search_wiki
    
    # Schemas
    from app.schemas.responses import ChatRequest, ChatResponse
    
    # Routers
    from app.routers.chat_router import router as chat_router
    
    print("✅ All imports successful")


def test_security():
    """Test security validation"""
    print("\nTesting security validation...")
    
    from app.core.security import validate_tool_call
    
    # Test 1: Valid tool call
    is_valid, error = validate_tool_call("check_weather", {"city": "New York"})
    assert is_valid, f"Valid call rejected: {error}"
    print("✅ Valid tool call accepted")
    
    # Test 2: Invalid tool
    is_valid, error = validate_tool_call("invalid_tool", {})
    assert not is_valid, "Invalid tool was accepted!"
    print("✅ Invalid tool rejected")
    
    # Test 3: Tool with URL injection
    is_valid, error = validate_tool_call("check_weather", {"city": "http://evil.com"})
    assert not is_valid, "URL injection accepted!"
    print("✅ URL injection blocked")
    
    # Test 4: Tool with special characters
    is_valid, error = validate_tool_call("check_weather", {"city": "New York<script>alert(1)</script>"})
    assert not is_valid, "Special characters accepted!"
    print("✅ Special characters blocked")
    
    print("✅ All security tests passed")


def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    from app.core.config import settings
    
    # Test that settings load
    assert settings.ollama_url, "Ollama URL not configured"
    assert settings.ollama_model, "Ollama model not configured"
    
    print(f"✅ Configuration loaded:")
    print(f"   - Ollama URL: {settings.ollama_url}")
    print(f"   - Ollama Model: {settings.ollama_model}")


def test_tools_registry():
    """Test tools are registered"""
    print("\nTesting tools registry...")
    
    from app.tools.tool_registry import AVAILABLE_TOOLS
    
    expected_tools = [
        "play_song",
        "pause_playback",
        "resume_playback",
        "next_track",
        "previous_track",
        "get_current_track",
        "check_weather",
        "get_forecast",
        "search_wiki",
        "get_wiki_summary",
    ]
    
    for tool in expected_tools:
        assert tool in AVAILABLE_TOOLS, f"Tool '{tool}' not registered"
    
    print(f"✅ All {len(AVAILABLE_TOOLS)} tools registered:")
    for tool in sorted(AVAILABLE_TOOLS.keys()):
        print(f"   - {tool}")


if __name__ == "__main__":
    print("=" * 60)
    print("LLM SPEAK - PROJECT VALIDATION")
    print("=" * 60)
    
    try:
        test_imports()
        test_configuration()
        test_tools_registry()
        test_security()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED - Project is ready!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
