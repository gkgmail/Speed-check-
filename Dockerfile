# Optimized Dockerfile for fast Koyeb deployment
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Minimal apt dependencies (removed unnecessary packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy and install requirements
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install --no-cache-dir -U -r requirements.txt

# Copy application
COPY . .

EXPOSE 8000

# Single process, no background flask
CMD ["python3", "-m", "devgagan"]
