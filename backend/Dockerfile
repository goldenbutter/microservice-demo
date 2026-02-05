# -------------------------------
# Backend Dockerfile (FastAPI)
# -------------------------------

# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY app ./app

# Expose the backend port
EXPOSE 8000

# Command to start FastAPI app on container launch
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]