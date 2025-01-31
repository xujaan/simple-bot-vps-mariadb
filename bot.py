import os
import psutil
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Fungsi untuk memantau resource server
def get_server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return f"CPU: {cpu_usage}%\nRAM: {memory_usage}%\nDisk: {disk_usage}%"

# Command /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Halo! Saya bot pemantau server. Gunakan /status untuk melihat resource server.")

# Command /status
def status(update: Update, context: CallbackContext):
    status_message = get_server_status()
    update.message.reply_text(status_message)

# Command /backup
def backup(update: Update, context: CallbackContext):
    os.system("./backup.sh")
    with open("/app/backups/backup.sql", "rb") as file:
        update.message.reply_document(document=file, caption="Backup database selesai.")

# Main function
def main():
    # Ambil token bot dari environment variable
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Tambahkan command handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("backup", backup))

    # Jalankan bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()