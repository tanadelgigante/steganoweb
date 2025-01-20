# Base image with Python and Qt dependencies
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-pyqt6 \
    libgl1-mesa-glx \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download the original Python script
RUN wget https://github.com/chtholine/Steganograpp/raw/refs/heads/main/main.py

# Install Python dependencies
RUN pip3 install Pillow==9.5.0 PyQt6==6.4.2

CMD ["python3", "main.py"]