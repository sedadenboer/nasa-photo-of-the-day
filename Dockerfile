FROM python:3.12-slim

# Install uv and set up virtual environment
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Project metadata for dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-cache

# Application source code
COPY app/ ./app

# Add virtualenv to PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]