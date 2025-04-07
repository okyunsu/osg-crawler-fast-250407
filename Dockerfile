FROM python:3.11-slim

WORKDIR /app

COPY ./app /app
COPY requirements.txt .  
COPY .env .    
# .env 파일도 복사

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
