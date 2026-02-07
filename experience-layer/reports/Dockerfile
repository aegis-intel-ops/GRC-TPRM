FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PDF generation
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5003

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5003"]
