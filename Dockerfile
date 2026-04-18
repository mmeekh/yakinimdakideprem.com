FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Non-root user (uid 10001)
RUN groupadd -r -g 10001 app && \
    useradd -r -u 10001 -g app --home /app --shell /sbin/nologin app

WORKDIR /app

# Guvenlik: tini + ca-certs + guncel sistem, sonra temizle
RUN apt-get update && \
    apt-get install -y --no-install-recommends tini ca-certificates && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python bagimliliklari
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama
COPY app app
COPY checklist.pdf ./

# Non-root dosya sahipligi + twitter bot icin /data
RUN mkdir -p /data && chown -R app:app /app /data

USER app

EXPOSE 8000

# tini - proper signal handling + zombie reaping
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
