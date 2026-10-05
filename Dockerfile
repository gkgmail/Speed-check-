# ⚡ Ultra-optimized Dockerfile for fastest Koyeb deployment
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    PYTHONOPTIMIZE=2

WORKDIR /app

# ⚡ OPTIMIZED: Minimal system dependencies + remove unnecessary tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archives/*

# ⚡ OPTIMIZED: Faster pip installation with parallel downloads
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install -j 4 --no-cache-dir -U -r requirements.txt \
    && find /usr/local/lib/python3.11/site-packages -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Copy application
COPY . .

EXPOSE 8000

# ⚡ Single process, optimized for speed
CMD ["python3", "-m", "devgagan"]
