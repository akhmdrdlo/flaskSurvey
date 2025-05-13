# Gunakan Python base image
FROM python:3.11-slim

# Set direktori kerja di container
WORKDIR /app

# Copy file app ke dalam container
COPY . /app

# Copy service account ke container (jika diperlukan)
COPY firestore-key.json .

# Install Firestore SDK
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Jalankan server menggunakan gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
