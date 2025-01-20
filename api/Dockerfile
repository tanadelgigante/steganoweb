# Use Python slim image for smaller size
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download main.py first
RUN wget -O main.py https://github.com/chtholine/Steganograpp/raw/refs/heads/main/main.py

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code last
COPY . .

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]