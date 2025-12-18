# Use Python slim image for smaller size
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Qt and X11 libs
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pyqt6 \
    libglib2.0-0 \
    libgl1 \
    libegl1 \
    libxkbcommon0 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Setup entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
