# NASA Photo of the Day

A simple FastAPI web app that shows NASA's Astronomy Picture of the Day (APOD) for a selected date.

## Features

* View NASA APOD for a chosen date
* Shows image, title, and explanation
* Simple, dark-mode interface

## Requirements

* [Python 3.12](https://www.python.org/downloads/)
* [Docker](https://www.docker.com/get-started)
* [NASA API key](https://api.nasa.gov/) (optional, defaults to `DEMO_KEY`)

## Project Structure

```text
.
├── app
│   ├── main.py                 # FastAPI application entry point
│   ├── static
│   │   ├── logo.png            # Application logo
│   │   └── styles.css          # Stylesheet for dark-mode interface
│   ├── templates
│   │   └── index.html          # HTML template for the web interface
│   └── testing
│       └── test-data.json      # Sample APOD data for testing interface
├── Dockerfile                  # Docker configuration 
├── .env.example                # Example environment variables
├── README.md                   # Project documentation
├── pyproject.toml              # Python project metadata and dependencies
└── uv.lock                     # Locked dependency versions for uv
```

## Configuration of `.env`

* **NASA_API_KEY** – optional environment variable for your API key
* **TEST_FLAG** – set to `true` to use local test data

## Local Development

1. Clone the repository:

```bash
git clone https://github.com/sedadenboer/nasa-photo-of-the-day
cd nasa-photo-of-the-day
```

2. Install dependencies (if using `uv`):

```bash
pip install uv
uv sync --frozen
```

3. Run the app:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. Open [http://localhost:8000](http://localhost:8000) in your browser and enter a date to view the APOD.

## Docker

### Build the image

```bash
docker build -t nasa-photo-of-the-day .
```

### Run the container

```bash
docker run -d -p 8000:80 nasa-photo-of-the-day
```

Then open [http://localhost:8000](http://localhost:8000).