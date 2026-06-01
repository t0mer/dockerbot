FROM ubuntu:24.10

LABEL maintainer="tomer.klein@gmail.com"

# Install required system dependencies
RUN apt update -yqq && \
    apt install -yqq python3 \
                    python3-pip \
                    curl \
                    wget \
                    speedtest-cli \
                    --no-install-recommends && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV API_KEY ""
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /opt/dockerbot

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Install speedtest-cli script
RUN wget https://raw.githubusercontent.com/sivel/speedtest-cli/v2.1.3/speedtest.py -O /usr/local/lib/python3.12/site-packages/speedtest.py

# Copy application code
COPY dockerbot.py .

# Run the application
CMD ["python3", "dockerbot.py"]
