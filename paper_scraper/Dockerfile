FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY modules ./modules
COPY main.py .

CMD ["python", "main.py"]
