from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio
import os

app = Flask(__name__)

# Thông tin tài khoản Telegram cá nhân
API_ID = 29148352  
API_HASH = "16c771c16661f6a21a6ba57ce5cb3b51"  
PHONE_NUMBER = "+14106235803"  
BOT_USERNAME = "@USDxchangebot"  

# Khởi tạo Telethon client
client = TelegramClient("user_session", API_ID, API_HASH)
loop = asyncio.get_event_loop()

# Hàm khởi động client
async def start_client():
    if not client.is_connected():
        await client.start(phone=PHONE_NUMBER)
        print("✅ Đăng nhập Telegram thành công")

# API endpoint để gửi tin nhắn
@app.route('/debug_telethon', methods=['GET'])
def debug_telethon():
    return jsonify({
        "is_connected": client.is_connected(),
        "session": str(client.session),
        "event_loop_running": asyncio.get_event_loop().is_running()
    })

@app.route('/send_telegram', methods=['POST'])  
def send_telegram():
    print(f"Nhận yêu cầu: {request.method} với data: {request.get_json()}")

    data = request.get_json()
    payment_code = data.get("payment_code") if data else None

    if not payment_code:
        return jsonify({"status": "error", "message": "Thiếu payment_code"}), 400

    command = f"/confirm {payment_code}"

    async def send_message():
        await client.send_message(BOT_USERNAME, command)

    # Gửi tin nhắn không đồng bộ
    loop.create_task(send_message())

    return jsonify({"status": "success", "message": f"Sent: {command}"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    loop.run_until_complete(start_client())  # Chạy client trước khi khởi động Flask
    app.run(host="0.0.0.0", port=port)
