FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8080

# TODO: Alembic migrations temporarily disabled—restore when dependency chain is fixed
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port \${PORT:-8080} --proxy-headers"