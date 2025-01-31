import os
import logging
from telegram import Bot

# Ambil environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BACKUP_FILE = "/app/backups/backup.sql"

# Setup logging
logging.basicConfig(filename="/var/log/backup.log", level=logging.INFO)

try:
    # Periksa apakah file backup ada dan tidak kosong
    if os.path.exists(BACKUP_FILE) and os.path.getsize(BACKUP_FILE) > 0:
        # Inisialisasi bot
        bot = Bot(token=BOT_TOKEN)

        # Kirim file backup
        with open(BACKUP_FILE, "rb") as file:
            bot.send_document(chat_id=CHAT_ID, document=file, caption="Backup database otomatis selesai.")
        logging.info("Backup file sent successfully.")
    else:
        logging.error("Backup file is empty or does not exist.")
except Exception as e:
    logging.error(f"Failed to send backup file: {e}")