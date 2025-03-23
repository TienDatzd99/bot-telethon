from telethon import TelegramClient, events

# Hardcode thông tin bot
API_ID = 29148352  # Điền trực tiếp số API_ID
API_HASH = "16c771c16661f6a21a6ba57ce5cb3b51"  # Điền API_HASH
BOT_TOKEN = "7556941363:AAG3SRd2xVh6-9kX98gJDmnW9fZNfb51NdM"  # Điền BOT_TOKEN

# Khởi tạo bot Telethon
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Xử lý tin nhắn đến bot
@bot.on(events.NewMessage(pattern="/confirm (.+)"))
async def confirm_handler(event):
    payment_code = event.pattern_match.group(1)
    await event.reply(f"Xác nhận thanh toán với mã: {payment_code}")

# Chạy bot
print("Bot đang chạy...")
bot.run_until_disconnected()
