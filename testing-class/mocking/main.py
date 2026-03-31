import requests


def get_weather(city: str) -> dict:
    """Fetch weather data for a city from external API."""
    response = requests.get(f"https://api.weather.com/v1/{city}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Could not fetch weather data")
