from fastapi import FastAPI, Request
import os
import dotenv
import httpx
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Initialize FastAPI app
app = FastAPI(
    title='Weather API',
    version='1.0.0',
    description='A simple API to fetch current weather data for a given city.',
)

# Load templates
templates = Jinja2Templates(directory="templates")

# Load environment variables
dotenv.load_dotenv()
API_KEY = os.getenv("WEATHER_API")

# Base URL for OpenWeatherMap API
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(WEATHER_URL, params=params)

    weather_info = None
    error = None

    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data['name'],
            "country": data['sys']['country'],
            "temp": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "humidity": data['main']['humidity'],
            "description": data['weather'][0]['description'].title()
        }
    else:
        error = f"Error fetching weather data (Status Code {response.status_code})"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "weather": weather_info,
        "city": city,
        "error": error
    })