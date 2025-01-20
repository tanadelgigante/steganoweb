# Use Python slim image for smaller size
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]