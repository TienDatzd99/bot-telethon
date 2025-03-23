import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Lấy thông tin từ biến môi trường
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Khởi tạo bot Telethon
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Xử lý tin nhắn đến bot
@bot.on(events.NewMessage)
async def handler(event):
    chat_id = event.chat_id
    message = event.raw_text
    print(f"Nhận tin nhắn từ {chat_id}: {message}")
    
    if message.lower() == "hello":
        await event.reply("Xin chào! Tôi là bot Telethon 🚀")

# Chạy bot
print("Bot đang chạy...")
bot.run_until_disconnected()
