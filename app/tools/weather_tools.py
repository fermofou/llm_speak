from app.services.weather_service import get_weather, get_weather_forecast


def check_weather(city: str) -> dict:
    """Get current weather for a city."""
    return get_weather(city)


def get_forecast(city: str, days: int = 5) -> dict:
    """Get weather forecast for a city."""
    return get_weather_forecast(city, days)
