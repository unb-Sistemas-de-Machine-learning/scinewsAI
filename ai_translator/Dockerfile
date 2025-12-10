# Builder
FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Runner
FROM python:3.11-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl libpq-dev

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src ./src
COPY main.py .
COPY seed.py .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "main.py"]