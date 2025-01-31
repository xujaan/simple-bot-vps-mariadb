#!/bin/bash
# Backup database
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME > /app/backups/backup.sql

# Kirim file backup ke Telegram menggunakan script Python
python3 /app/send_to_telegram.py