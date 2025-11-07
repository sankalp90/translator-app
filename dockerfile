# Use official Python slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies including Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Run migrations (optional)
RUN python manage.py migrate

# Set the command to run the app with Gunicorn
CMD ["gunicorn", "translator_project.wsgi:application", "--bind", "0.0.0.0:10000"]
