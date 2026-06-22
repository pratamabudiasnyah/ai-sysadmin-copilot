# Base image
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements (belum ada, kita buat dulu)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file aplikasi
COPY . .

# Port yang akan dipakai
EXPOSE 8000

# Command untuk jalankan app
CMD ["python", "main.py"]
