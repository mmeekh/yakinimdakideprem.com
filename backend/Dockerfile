FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
COPY checklist.pdf .

EXPOSE 8000
# Üretimde FastAPI CLI ile Uvicorn çalıştır
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
