from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import os
from dotenv import load_dotenv

load_dotenv() 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

APOD_API_URL = "https://api.nasa.gov/planetary/apod"
APOD_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")


async def fetch_apod(params: dict):
    async with httpx.AsyncClient() as client:
        response = await client.get(APOD_API_URL, params=params)
        response.raise_for_status()
        return response.json()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, date: str = Query(None, description="YYYY-MM-DD")):
    params = {"api_key": APOD_API_KEY}

    if date:
        params["date"] = date 
        
    data = await fetch_apod(params)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "data": [data]}
    )