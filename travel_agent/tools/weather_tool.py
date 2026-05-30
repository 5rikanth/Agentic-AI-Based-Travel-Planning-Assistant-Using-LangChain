"""
Weather Lookup Tool for the AI Travel Planning Agent.
Uses the free Open-Meteo API (no API key required).
"""

import requests
from langchain.tools import tool


# City coordinates mapping for Open-Meteo API
CITY_COORDINATES = {
    "Goa": (15.2993, 74.1240),
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Jaipur": (26.9124, 75.7873),
    "Kerala": (10.8505, 76.2711),
    "Manali": (32.2396, 77.1887),
    "Agra": (27.1767, 78.0081),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
}

WMO_DESCRIPTIONS = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Icy fog 🌫️",
    51: "Light drizzle 🌦️",
    53: "Moderate drizzle 🌦️",
    55: "Dense drizzle 🌧️",
    61: "Slight rain 🌧️",
    63: "Moderate rain 🌧️",
    65: "Heavy rain 🌧️",
    71: "Light snow 🌨️",
    73: "Moderate snow ❄️",
    75: "Heavy snow ❄️",
    80: "Slight showers 🌦️",
    81: "Moderate showers 🌧️",
    82: "Violent showers ⛈️",
    95: "Thunderstorm ⛈️",
    99: "Thunderstorm with hail ⛈️",
}


@tool
def get_weather(query: str) -> str:
    """
    Get weather forecast for a destination city for the next 7 days.

    Input: city name
    Examples: "Goa", "Jaipur", "Manali", "Kerala"

    Returns day-wise temperature, weather condition, and travel tips.
    """
    try:
        city = query.strip().title()

        if city not in CITY_COORDINATES:
            available = ", ".join(sorted(CITY_COORDINATES.keys()))
            return (
                f"Weather data not available for '{city}'. "
                f"Available cities: {available}"
            )

        lat, lon = CITY_COORDINATES[city]

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum"
            f"&timezone=auto"
            f"&forecast_days=7"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        weather_codes = daily.get("weathercode", [])
        precipitation = daily.get("precipitation_sum", [])

        result_lines = [
            f"🌤️ 7-Day Weather Forecast for {city}:",
            f"",
        ]

        for i in range(min(7, len(dates))):
            code = weather_codes[i] if i < len(weather_codes) else 0
            condition = WMO_DESCRIPTIONS.get(code, "Variable weather")
            max_t = max_temps[i] if i < len(max_temps) else "N/A"
            min_t = min_temps[i] if i < len(min_temps) else "N/A"
            rain = precipitation[i] if i < len(precipitation) else 0

            # Packing tip
            tip = ""
            if code in [61, 63, 65, 80, 81, 82, 95, 99]:
                tip = " 🌂 Carry umbrella"
            elif isinstance(max_t, (int, float)) and max_t > 35:
                tip = " 🧴 Apply sunscreen"
            elif isinstance(min_t, (int, float)) and min_t < 10:
                tip = " 🧥 Carry warm clothes"

            result_lines.append(
                f"  📅 {dates[i]}: {condition}"
                f" | 🌡️ {max_t}°C / {min_t}°C"
                f" | 🌧️ Rain: {rain}mm"
                f"{tip}"
            )

        # General recommendation
        avg_max = sum(t for t in max_temps if isinstance(t, (int, float))) / len(max_temps) if max_temps else 25
        result_lines.extend([
            f"",
            f"📌 Summary: Average high of {avg_max:.1f}°C expected in {city}.",
        ])

        return "\n".join(result_lines)

    except requests.exceptions.ConnectionError:
        return (
            f"⚠️ Could not connect to weather API (no internet access in this environment). "
            f"In production, this would fetch live data from Open-Meteo for {query.strip().title()}."
        )
    except requests.exceptions.Timeout:
        return "Weather API request timed out. Please try again."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
