FROM python:3.11-slim-bookworm

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies your binaries might need
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
 && pip install requests \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy your serverManager binaries
COPY /data /data
RUN chmod +x /data/a2s-cli && chmod +x /data/a3sb-cli

# Set working directory for your app
WORKDIR /app

# Install Python dependencies (Flask, Gunicorn, etc.)
RUN pip install --no-cache-dir flask gunicorn

# Run your app with Gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT api:app

STOPSIGNAL SIGINT

# Your custom environment variables
ENV A3_SERVER_ADDRESS=sm1.krabicka.eu:6913
ENV A2S_COMMAND=/data/a3sb-cli
ENV PYTHONPATH=/data/python

