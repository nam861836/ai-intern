FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
# uv python
WORKDIR /app

# Install uv
# RUN pip install --no-cache-dir uv
COPY app ./app
COPY config ./config
COPY data ./data
# Copy dependency files first for better caching
COPY app/pyproject.toml /app/
COPY app/uv.lock /app/

# Copy code

# Set PYTHONPATH for correct imports
ENV PYTHONPATH=/app/app

# Install dependencies using uv
RUN uv sync --frozen --no-dev


EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]