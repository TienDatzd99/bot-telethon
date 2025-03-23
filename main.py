import os
from telethon import TelegramClient, events

# Lấy thông tin từ biến môi trường
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Kiểm tra biến môi trường
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Thiếu biến môi trường! Hãy kiểm tra API_ID, API_HASH và BOT_TOKEN.")

API_ID = int(API_ID)  # Chuyển đổi API_ID sang số nguyên

# Khởi tạo bot Telethon
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Xử lý tin nhắn đến bot
@bot.on(events.NewMessage(pattern="/confirm (.+)"))
async def confirm_handler(event):
    payment_code = event.pattern_match.group(1)
    chat_id = event.chat_id
    await event.reply(f"Xác nhận thanh toán với mã: {payment_code}")
    
# Chạy bot
print("Bot đang chạy...")
bot.run_until_disconnected()
