FROM python:3.12-slim

LABEL maintainer="tomer.klein@gmail.com"

ENV API_KEY="" \
    ALLOWED_IDS="" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# curl is used by ip_command at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dockerbot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dockerbot.py .

CMD ["python3", "dockerbot.py"]
