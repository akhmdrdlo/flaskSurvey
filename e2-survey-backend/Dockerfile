FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose the default port Cloud Run uses
EXPOSE 8080

# Gunicorn command (assume your app object is in app.main)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.main:app"]
