import os
import sys
import logging
from telegram import Bot

# Ambil environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Ambil nama file backup dari argumen
if len(sys.argv) > 1:
    BACKUP_FILE = sys.argv[1]
else:
    BACKUP_FILE = "/app/backups/backup.sql"  # Fallback jika tidak ada argumen

# Setup logging
logging.basicConfig(filename="/var/log/backup.log", level=logging.INFO)

async def send_backup():
    try:
        # Periksa apakah file backup ada dan tidak kosong
        if os.path.exists(BACKUP_FILE) and os.path.getsize(BACKUP_FILE) > 0:
            # Inisialisasi bot
            bot = Bot(token=BOT_TOKEN)

            # Kirim file backup
            with open(BACKUP_FILE, "rb") as file:
                await bot.send_document(
                    chat_id=CHAT_ID,
                    document=file,
                    caption=f"Backup database selesai: {os.path.basename(BACKUP_FILE)}"
                )
            logging.info(f"Backup file {BACKUP_FILE} sent successfully.")

            # Hapus file backup setelah berhasil dikirim
            os.remove(BACKUP_FILE)
            logging.info(f"Backup file {BACKUP_FILE} deleted successfully.")
        else:
            logging.error("Backup file is empty or does not exist.")
    except Exception as e:
        logging.error(f"Failed to send or delete backup file: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_backup())