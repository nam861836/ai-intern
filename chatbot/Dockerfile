# FROM python:3.10-slim

# WORKDIR /app

# RUN python -m ensurepip --upgrade && \
#     pip install --no-cache-dir --upgrade pip && \
#     pip install poetry

# # Copy code and config before install so Poetry can find the package
# COPY app ./app
# COPY config ./config
# COPY data ./data

# COPY pyproject.toml /app/

# # Set PYTHONPATH for correct imports
# ENV PYTHONPATH=/app/app

# RUN poetry config virtualenvs.create false \
#     && poetry install --no-root

# EXPOSE 8000
# CMD ["poetry", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first for better caching
COPY app ./app
COPY config ./config
COPY data ./data
COPY pyproject.toml /app/
COPY uv.lock /app/

# Set PYTHONPATH for correct imports
ENV PYTHONPATH=/app/app

# Install dependencies using uv
RUN uv sync --frozen --no-dev


EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]