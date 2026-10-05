# ⚡ ULTRA-OPTIMIZED Dockerfile for 15MB Speed - FAST DEPLOYMENT
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    PYTHONOPTIMIZE=2 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app

# ⚡ STAGE 1: Minimal dependencies - no ffmpeg bloat
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ⚡ Copy and install minimal requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check \
    --no-build-isolation -q --progress-bar off \
    -r requirements.txt && \
    find /usr/local/lib/python3.11/site-packages -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11 -type f -name "*.pyc" -delete && \
    find /usr/local/lib/python3.11 -type f -name "*.pyo" -delete

# ⚡ Copy app
COPY . .

# ⚡ Expose port
EXPOSE 8000

# ⚡ Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ⚡ Ultra-fast startup
CMD ["python3", "-m", "devgagan"]
