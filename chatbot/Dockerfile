FROM python:3.10-slim

WORKDIR /app

RUN python -m ensurepip --upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install poetry

# Copy code and config before install so Poetry can find the package
COPY app ./app
COPY config ./config
COPY pyproject.toml /app/

# Set PYTHONPATH for correct imports
ENV PYTHONPATH=/app/app

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]