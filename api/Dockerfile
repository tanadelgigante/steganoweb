# Use Python slim image for smaller size
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Download the main.py file from the remote repository
RUN wget -O /app/main.py https://github.com/chtholine/Steganograpp/raw/refs/heads/main/main.py

# Copy application code
COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]