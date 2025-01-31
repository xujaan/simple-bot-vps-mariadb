# Gunakan image base Python 3.9
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Install cron dan dependencies
RUN apt-get update && apt-get install -y cron && apt-get clean

# Copy file requirements.txt ke container
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh proyek ke container
COPY . .

# Buat direktori untuk menyimpan backup
RUN mkdir -p /app/backups

# Jadikan script backup.sh executable
RUN chmod +x /app/backup.sh

# Copy file cron job
COPY cronjob /etc/cron.d/cronjob

# Berikan izin execute pada file cron job
RUN chmod 0644 /etc/cron.d/cronjob

# Jalankan cron
RUN crontab /etc/cron.d/cronjob

# Command untuk menjalankan bot dan cron
CMD ["sh", "-c", "cron && python3 bot.py"]