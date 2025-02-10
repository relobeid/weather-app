import os
import requests
from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# OpenWeather API URL
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

app = FastAPI()

@app.get("/weather")
def get_weather(city: str = Query(..., description="Enter city name")):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key is missing or invalid.")

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Get temperature in Celsius
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=5)

        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "weather": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found.")
        else:
            raise HTTPException(status_code=response.status_code, detail="Weather API error.")

    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Weather API timed out.")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to reach weather API: {str(e)}")
