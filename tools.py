"""
Tool implementations for the AI agent.
Each tool can be called by the agent to perform specific tasks.
"""

import requests
import json
from datetime import datetime
import pytz
import os


def get_weather(location: str) -> str:
    """
    Get current weather for a location using OpenWeatherMap API.
    
    Args:
        location: City name (e.g., "London", "New York", "Tokyo")
    
    Returns:
        JSON string with weather information
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return json.dumps({"error": "OpenWeatherMap API key not configured"})
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "location": data["name"],
                "country": data["sys"]["country"],
                "temperature": f"{data['main']['temp']}°F",
                "feels_like": f"{data['main']['feels_like']}°F",
                "conditions": data["weather"][0]["description"],
                "humidity": f"{data['main']['humidity']}%",
                "wind_speed": f"{data['wind']['speed']} mph"
            }
            return json.dumps(weather_info, indent=2)
        else:
            return json.dumps({"error": f"Failed to fetch weather data: {response.status_code}"})
    
    except Exception as e:
        return json.dumps({"error": f"Error fetching weather: {str(e)}"})


def get_location() -> str:
    """
    Get user's current location based on IP address using multiple fallback APIs.
    
    Returns:
        JSON string with location information
    """
    # List of APIs to try in order
    apis = [
        {
            "name": "ipapi.co",
            "url": "https://ipapi.co/json/",
            "parser": lambda data: {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "country_code": data.get("country_code", "Unknown"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone", "Unknown"),
                "ip": data.get("ip", "Unknown")
            }
        },
        {
            "name": "ip-api.com",
            "url": "http://ip-api.com/json/",
            "parser": lambda data: {
                "city": data.get("city", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "country": data.get("country", "Unknown"),
                "country_code": data.get("countryCode", "Unknown"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone", "Unknown"),
                "ip": data.get("query", "Unknown")
            }
        },
        {
            "name": "ipinfo.io",
            "url": "https://ipinfo.io/json",
            "parser": lambda data: {
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "country": data.get("country", "Unknown"),
                "country_code": data.get("country", "Unknown"),
                "latitude": data.get("loc", "").split(",")[0] if data.get("loc") else None,
                "longitude": data.get("loc", "").split(",")[1] if data.get("loc") else None,
                "timezone": data.get("timezone", "Unknown"),
                "ip": data.get("ip", "Unknown")
            }
        }
    ]
    
    for api in apis:
        try:
            print(f"Trying {api['name']}...")
            response = requests.get(api["url"], timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                location_info = api["parser"](data)
                location_info["source"] = api["name"]
                print(f"✅ Successfully got location from {api['name']}")
                return json.dumps(location_info, indent=2)
            else:
                print(f"❌ {api['name']} returned status {response.status_code}")
                continue
                
        except Exception as e:
            print(f"❌ {api['name']} failed: {str(e)}")
            continue
    
    # If all APIs fail, return a helpful error message
    return json.dumps({
        "error": "Unable to detect location. All location services are currently unavailable or rate-limited. Please try again later or manually specify your location.",
        "suggestion": "You can tell me your city name and I can help you with weather, time, or other location-based information."
    }, indent=2)


def get_time(timezone: str = "UTC") -> str:
    """
    Get current time for a specific timezone.
    
    Args:
        timezone: Timezone name (e.g., "UTC", "America/New_York", "Asia/Tokyo")
    
    Returns:
        JSON string with time information
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        
        time_info = {
            "timezone": timezone,
            "current_time": current_time.strftime("%H:%M:%S"),
            "current_date": current_time.strftime("%Y-%m-%d"),
            "day_of_week": current_time.strftime("%A"),
            "formatted": current_time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
        }
        return json.dumps(time_info, indent=2)
    
    except Exception as e:
        return json.dumps({"error": f"Error getting time: {str(e)}. Try common timezones like 'UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'"})


def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.
    
    Args:
        expression: Mathematical expression (e.g., "2 + 2", "10 * 5 + 3")
    
    Returns:
        JSON string with calculation result
    """
    try:
        # Safe evaluation - only allow basic math operations
        allowed_chars = set("0123456789+-*/().[] ")
        if not all(c in allowed_chars for c in expression):
            return json.dumps({"error": "Invalid characters in expression. Only numbers and basic operators (+, -, *, /, parentheses) are allowed."})
        
        result = eval(expression, {"__builtins__": {}}, {})
        
        calc_info = {
            "expression": expression,
            "result": result
        }
        return json.dumps(calc_info, indent=2)
    
    except Exception as e:
        return json.dumps({"error": f"Error calculating: {str(e)}"})


# Tool definitions for OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location/city. Use this when the user asks about weather conditions, temperature, or climate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., London, New York, Tokyo"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_location",
            "description": "Detect the user's current location based on their IP address. Returns city, country, and coordinates. Use this when you need to know where the user is located.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current time and date for a specific timezone. Use this when the user asks about the current time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The timezone name (e.g., 'UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo'). Defaults to UTC if not specified."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations. Evaluate expressions with basic arithmetic operations (+, -, *, /, parentheses).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g., '2 + 2', '(10 * 5) + 3'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# Map function names to actual functions
AVAILABLE_FUNCTIONS = {
    "get_weather": get_weather,
    "get_location": get_location,
    "get_time": get_time,
    "calculate": calculate
}

