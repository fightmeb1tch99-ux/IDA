# Use Python 3.11 Slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libasound2-dev \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create knowledge directory
RUN mkdir -p knowledge

# Expose ports for Dashboard and API
EXPOSE 8000

# Run both Telegram Bot and Dashboard (using a simple entrypoint script)
CMD python3 telegram_bot.py & python3 web_dashboard.py
