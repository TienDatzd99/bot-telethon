from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio
import os

app = Flask(__name__)

# Thông tin tài khoản Telegram cá nhân
API_ID = 21888878  
API_HASH = "ce0e9187e71e206a8c3b9343756e8136"  
BOT_USERNAME = "@PayUsd_bot"  

# Khởi tạo Telethon client
client = TelegramClient("user_session", API_ID, API_HASH)

async def start_client():
    await client.connect()
    if not await client.is_user_authorized():
        print("🚨 Chưa có session hợp lệ! Hãy đăng nhập trên máy tính trước.")

# API debug kiểm tra kết nối Telethon
@app.route('/debug_telethon', methods=['GET'])
def debug_telethon():
    return jsonify({
        "is_connected": client.is_connected(),
        "session": str(client.session)
    })

# API gửi tin nhắn Telegram
@app.route('/send_telegram', methods=['POST'])  
async def send_telegram():
    data = request.get_json()
    payment_code = data.get("payment_code")

    if not payment_code:
        return jsonify({"status": "error", "message": "Thiếu payment_code"}), 400

    command = f"/confirm {payment_code}"
    await client.send_message(BOT_USERNAME, command)

    return jsonify({"status": "success", "message": f"Sent: {command}"}), 200

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_client())  # Chạy client trước khi khởi động Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
