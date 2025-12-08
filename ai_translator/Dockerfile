# Builder
FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock* ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Runner
FROM python:3.11-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY main.py .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["python", "main.py"]