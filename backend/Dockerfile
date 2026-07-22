############################################################
# Backend Dockerfile
############################################################

FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

############################################################
# Install System Packages
############################################################

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

############################################################
# Install Python Dependencies
############################################################

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

############################################################
# Copy Project
############################################################

COPY . .

############################################################
# Expose FastAPI Port
############################################################

EXPOSE 8000

############################################################
# Start FastAPI
############################################################

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]