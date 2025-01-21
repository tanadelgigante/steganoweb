# Use Python slim image for smaller size
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Qt
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pyqt6 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]