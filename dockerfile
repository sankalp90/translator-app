# Use official Python base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libtesseract-dev tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Run migrations (optional, can also do on first container run)
RUN python manage.py migrate

# Expose port
EXPOSE 10000

# Run the app with Gunicorn
CMD ["gunicorn", "translator_project.wsgi:application", "--bind", "0.0.0.0:10000"]
