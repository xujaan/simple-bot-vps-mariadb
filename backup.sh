#!/bin/bash
# Buat nama file backup dengan timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/app/backups/backup_${TIMESTAMP}.sql"

# Backup database
mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_FILE

BACKUP_FILE2="/app/backups/backup_${TIMESTAMP}_db2.sql"
mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME2 > $BACKUP_FILE2

# Kirim file backup ke Telegram menggunakan script Python
python3 /app/send_to_telegram.py $BACKUP_FILE
python3 /app/send_to_telegram.py $BACKUP_FILE2