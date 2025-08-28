# FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
# # uv python
# WORKDIR /app

# # Install uv
# # RUN pip install --no-cache-dir uv
# COPY app ./app
# COPY config ./config
# COPY data ./data
# # Copy dependency files first for better caching
# COPY app/pyproject.toml /app/
# COPY app/uv.lock /app/

# # Copy code

# # Set PYTHONPATH for correct imports
# ENV PYTHONPATH=/app/app

# # Install dependencies using uv
# RUN uv sync --frozen --no-dev


# EXPOSE 8000
# CMD ["uv", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Build stage ---
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/
COPY app ./app
# COPY config ./config
# COPY data ./data

# Install dependencies and project into /app/.venv
RUN uv venv .venv 
RUN uv sync --frozen --no-dev

# --- Runtime stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy app code and config
COPY app ./app
COPY config ./config
COPY data ./data

ENV PYTHONPATH=/app/app
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["fastapi", "run", "app/api/main.py", "--host", "0.0.0.0", "--port", "8000"]
