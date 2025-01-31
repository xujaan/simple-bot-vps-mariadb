import os
import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Fungsi untuk memantau resource server
def get_server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return f"CPU: {cpu_usage}%\nRAM: {memory_usage}%\nDisk: {disk_usage}%"

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya bot pemantau server. Gunakan /status untuk melihat resource server.")

# Command /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = get_server_status()
    await update.message.reply_text(status_message)

# Command /backup
async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    os.system("./backup.sh")
    with open("/app/backups/backup.sql", "rb") as file:
        await update.message.reply_document(document=file, caption="Backup database selesai.")

# Main function
def main():
    # Ambil token bot dari environment variable
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Buat aplikasi bot
    application = Application.builder().token(BOT_TOKEN).build()

    # Tambahkan command handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("backup", backup))

    # Jalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()