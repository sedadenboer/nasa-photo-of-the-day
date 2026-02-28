import json
import os
from datetime import date, datetime

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


load_dotenv()

APOD_API_URL = "https://api.nasa.gov/planetary/apod"
APOD_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")

MIN_DATE = date(1995, 6, 16)
TODAY = date.today()

TEST_DATA = None
if os.getenv("TEST_FLAG", "false").lower() == "true":
    with open("testing/test-data.json", encoding="utf-8") as f:
        TEST_DATA = json.load(f)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = httpx.AsyncClient(timeout=30.0)


async def fetch_apod(date_str: str | None = None) -> dict:
    params = {"api_key": APOD_API_KEY}
    if date_str:
        params["date"] = date_str

    response = await client.get(APOD_API_URL, params=params)
    response.raise_for_status()
    return response.json()


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    date: str | None = Query(None),
) -> HTMLResponse:
    parsed_date: datetime.datetime | None = None

    if date:
        try:
            parsed_date = datetime.strptime(
                date, "%Y-%m-%d"
            ).date()

            if not MIN_DATE <= parsed_date <= TODAY:
                return RedirectResponse(url="/", status_code=302)

        except ValueError:
            return RedirectResponse(url="/", status_code=302)

    date_str = parsed_date.isoformat() if parsed_date else None

    try:
        apod = TEST_DATA if TEST_DATA else await fetch_apod(date_str)
    except httpx.HTTPStatusError:
        return RedirectResponse(url="/", status_code=302)

    display_date = datetime.strptime(
        apod["date"], "%Y-%m-%d"
    ).strftime("%B %d, %Y")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": [apod],
            "min_date": MIN_DATE.isoformat(),
            "today": TODAY.isoformat(),
            "display_date": display_date,
        },
    )