from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio
import os

app = Flask(__name__)

# Thông tin tài khoản Telegram cá nhân
API_ID = "29148352"  # Thay bằng api_id của bạn
API_HASH = "16c771c16661f6a21a6ba57ce5cb3b51"  # Thay bằng api_hash của bạn
PHONE_NUMBER = "+14106235803"  # Thay bằng số điện thoại (ví dụ: +84123456789)
BOT_USERNAME = "@USDxchangebot"  # Thay bằng username bot

# Khởi tạo Telethon client
client = TelegramClient("user_session", API_ID, API_HASH)
is_authenticated = False

# Hàm khởi động client
async def start_client():
    global is_authenticated
    if not is_authenticated:
        await client.start(phone=PHONE_NUMBER)
        is_authenticated = True
        print("Đăng nhập Telegram thành công")

# API endpoint để nhận mã thanh toán và gửi tin nhắn
@app.route('/send_telegram', methods=['POST'])
async def send_telegram():
    data = request.get_json()
    payment_code = data.get("payment_code")

    if not payment_code:
        return jsonify({"status": "error", "message": "Missing payment_code"}), 400

    command = f"/confirm {payment_code}"
    
    # Đảm bảo client đã khởi động
    if not is_authenticated:
        await start_client()

    # Gửi tin nhắn tới bot
    try:
        await client.send_message(BOT_USERNAME, command)
        return jsonify({"status": "success", "message": f"Sent: {command}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Khởi động Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Chạy client trong asyncio loop
    asyncio.run(start_client())
    app.run(host="0.0.0.0", port=port)