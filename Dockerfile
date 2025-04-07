FROM python:3.9-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PORT=8888

# Add non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

EXPOSE 8888

# Keep root user for psql access
# USER appuser

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8888"]
