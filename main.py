import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Lấy thông tin từ biến môi trường
API_ID = os.getenv("API_ID")
if API_ID is None:
    raise ValueError("API_ID is missing! Please set it in environment variables.")
API_ID = int(API_ID)
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

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
