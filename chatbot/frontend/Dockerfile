FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set the working directory
WORKDIR /app

# Copy dependency file
# COPY frontend/pyproject.toml .
# COPY frontend/uv.lock .

# Copy the rest of your application code
COPY frontend/ .
COPY config/ ./config
# COPY data/ ./data

RUN uv sync --frozen --no-dev --verbose
# Set PYTHONPATH for your application's imports
ENV PYTHONPATH=/app

# Expose the correct port
EXPOSE 8501

# Use 'uv run' which correctly handles the environment path.
# This is the most reliable way to run a command installed by uv.
CMD ["uv", "run", "streamlit", "run", "demo.py", "--server.port=8501", "--server.address=0.0.0.0"]