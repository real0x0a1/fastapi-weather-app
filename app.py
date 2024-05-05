import requests
import os

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('API_TOKEN')

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/weather")
async def get_weather(request: Request, city: str = Form(...)):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == "404":
        return {"error": "City not found"}
    else:
        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
        return templates.TemplateResponse("weather.html", {"request": request, "weather_data": weather_data})