#!/bin/bash
# Buat nama file backup dengan timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/app/backups/backup_${TIMESTAMP}.sql"

# Backup database
mysqldump -u $DB_USER -p$DB_PASSWORD $DB_NAME > $BACKUP_FILE

# Kirim file backup ke Telegram menggunakan script Python
python3 /app/send_to_telegram.py $BACKUP_FILE