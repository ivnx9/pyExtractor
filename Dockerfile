FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    antiword \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Start the app
CMD ["python", "app.py"]
