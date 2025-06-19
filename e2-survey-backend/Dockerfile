# Base image Python 3.11
FROM python:3.11-slim

# Buat direktori kerja
WORKDIR /app

# Salin file requirements dan install dependency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file project ke dalam container
COPY . .

# Jalankan aplikasi Flask di dalam container
CMD ["python", "main.py"]
