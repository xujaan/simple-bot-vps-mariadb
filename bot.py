import os
import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

def get_server_status():
    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)

    # Memory Usage
    memory = psutil.virtual_memory()
    memory_total = round(memory.total / (1024 ** 3), 2)  # Dalam GB
    memory_used = round(memory.used / (1024 ** 3), 2)    # Dalam GB
    memory_free = round(memory.free / (1024 ** 3), 2)    # Dalam GB
    memory_cached = round(memory.cached / (1024 ** 3), 2)  # Dalam GB
    memory_buffers = round(memory.buffers / (1024 ** 3), 2)  # Dalam GB

    # Swap Usage
    swap = psutil.swap_memory()
    swap_total = round(swap.total / (1024 ** 3), 2)  # Dalam GB
    swap_used = round(swap.used / (1024 ** 3), 2)    # Dalam GB
    swap_free = round(swap.free / (1024 ** 3), 2)    # Dalam GB

    # Disk Usage
    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024 ** 3), 2)  # Dalam GB
    disk_used = round(disk.used / (1024 ** 3), 2)    # Dalam GB
    disk_free = round(disk.free / (1024 ** 3), 2)    # Dalam GB

    # Disk I/O
    disk_io = psutil.disk_io_counters()
    disk_read = round(disk_io.read_bytes / (1024 ** 2), 2)  # Dalam MB
    disk_write = round(disk_io.write_bytes / (1024 ** 2), 2)  # Dalam MB

    # Network I/O
    net_io = psutil.net_io_counters()
    net_sent = round(net_io.bytes_sent / (1024 ** 2), 2)  # Dalam MB
    net_recv = round(net_io.bytes_recv / (1024 ** 2), 2)  # Dalam MB

    # Top Processes (berdasarkan penggunaan CPU dan memory)
    top_processes_cpu = []
    top_processes_memory = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            process_info = proc.info
            cpu_percent = process_info['cpu_percent']
            memory_usage = round(process_info['memory_info'].rss / (1024 ** 2), 2)  # RSS dalam MB
            top_processes_cpu.append((cpu_percent, process_info['pid'], process_info['name'], memory_usage))
            top_processes_memory.append((memory_usage, process_info['pid'], process_info['name'], cpu_percent))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Ambil 5 proses teratas berdasarkan penggunaan CPU
    top_processes_cpu.sort(reverse=True, key=lambda x: x[0])
    top_processes_cpu = top_processes_cpu[:5]

    # Ambil 5 proses teratas berdasarkan penggunaan memory
    top_processes_memory.sort(reverse=True, key=lambda x: x[0])
    top_processes_memory = top_processes_memory[:5]

    # Format pesan status
    status_message = (
        "=== CPU Usage ===\n"
        f"Total CPU Cores: {cpu_count}\n"
        f"CPU Usage: {cpu_usage}%\n\n"

        "=== Memory Usage ===\n"
        f"Total Memory: {memory_total} GB\n"
        f"Used Memory: {memory_used} GB\n"
        f"Free Memory: {memory_free} GB\n"
        f"Cached Memory: {memory_cached} GB\n"
        f"Buffers: {memory_buffers} GB\n\n"

        "=== Swap Usage ===\n"
        f"Total Swap: {swap_total} GB\n"
        f"Used Swap: {swap_used} GB\n"
        f"Free Swap: {swap_free} GB\n\n"

        "=== Disk Usage ===\n"
        f"Total Disk: {disk_total} GB\n"
        f"Used Disk: {disk_used} GB\n"
        f"Free Disk: {disk_free} GB\n\n"

        "=== Disk I/O ===\n"
        f"Read: {disk_read} MB\n"
        f"Write: {disk_write} MB\n\n"

        "=== Network I/O ===\n"
        f"Sent: {net_sent} MB\n"
        f"Received: {net_recv} MB\n\n"

        "=== Top Processes (by CPU) ===\n"
    )

    # Tambahkan informasi top processes by CPU
    for i, (cpu_percent, pid, name, memory_usage) in enumerate(top_processes_cpu, start=1):
        status_message += f"{i}. PID: {pid}, Name: {name}, CPU: {cpu_percent}%, Memory: {memory_usage} MB\n"

    status_message += "\n=== Top Processes (by Memory) ===\n"

    # Tambahkan informasi top processes by memory
    for i, (memory_usage, pid, name, cpu_percent) in enumerate(top_processes_memory, start=1):
        status_message += f"{i}. PID: {pid}, Name: {name}, Memory: {memory_usage} MB, CPU: {cpu_percent}%\n"

    return status_message


# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya bot pemantau server. Gunakan /status untuk melihat resource server.")

# Command /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = get_server_status()
    await update.message.reply_text(status_message)

# Command /backup
async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Jalankan script backup.sh
    os.system("./backup.sh")
    # File backup akan dikirim dan dihapus oleh send_to_telegram.py
    await update.message.reply_text("Proses backup sedang berjalan. File akan dikirim ke Telegram jika berhasil.")

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
