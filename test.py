from telethon.sync import TelegramClient

API_ID = 29148352
API_HASH = "16c771c16661f6a21a6ba57ce5cb3b51"
PHONE_NUMBER = "+14106235803"

client = TelegramClient("user_session", API_ID, API_HASH)
client.start(PHONE_NUMBER)
print("✅ Đăng nhập thành công, session đã được lưu.")
client.disconnect()
