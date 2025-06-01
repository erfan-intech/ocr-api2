# Use Python base image
FROM python:3.11-slim

# Install tesseract and other packages
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Render uses 10000+)
EXPOSE 10000

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
