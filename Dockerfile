# Start with a lightweight Python image
FROM python:3.10-slim

# Install system packages and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy your Python code and dependency files
COPY requirements.txt .
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Railway will forward traffic to
EXPOSE 8000

# Run Streamlit, binding to all interfaces and Railway's required port
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8000"]
