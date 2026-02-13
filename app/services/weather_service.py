import requests
from app.core.config import settings


def get_weather(city: str) -> dict:
    """
    Get current weather for a city using OpenWeatherMap API.
    
    Args:
        city: City name
        
    Returns:
        Dictionary with weather information
    """
    if not settings.openweather_api_key:
        return {
            "success": False,
            "error": "OpenWeatherMap API key not configured"
        }
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            return {
                "success": True,
                "city": data.get("name"),
                "temperature": data.get("main", {}).get("temp"),
                "description": data.get("weather", [{}])[0].get("description"),
                "humidity": data.get("main", {}).get("humidity"),
                "wind_speed": data.get("wind", {}).get("speed")
            }
        else:
            return {
                "success": False,
                "error": data.get("message", "Weather service error")
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_weather_forecast(city: str, days: int = 5) -> dict:
    """Get weather forecast for a city."""
    if not settings.openweather_api_key:
        return {
            "success": False,
            "error": "OpenWeatherMap API key not configured"
        }
    
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric",
            "cnt": days * 8  # 8 forecasts per day
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            return {
                "success": True,
                "city": data.get("city", {}).get("name"),
                "forecasts": data.get("list", [])[:8]
            }
        else:
            return {
                "success": False,
                "error": data.get("message", "Forecast service error")
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
