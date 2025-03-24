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
@app.route('/send_telegram', methods=['GET', 'POST'])  # Bỏ async
def send_telegram():
    print(f"Nhận yêu cầu: {request.method} với data: {request.get_json(silent=True) or request.args}")

    if request.method == 'POST':
        data = request.get_json(silent=True)
        payment_code = data.get("payment_code") if data else None
    else:  # GET
        payment_code = request.args.get("payment_code")

    if not payment_code:
        return jsonify({"status": "error", "message": "Missing payment_code"}), 400

    command = f"/confirm {payment_code}"
    
    if not is_authenticated:
        asyncio.run(start_client())  # Chạy đồng bộ trong asyncio

    try:
        asyncio.run(client.send_message(BOT_USERNAME, command))  # Chạy đồng bộ
        return jsonify({"status": "success", "message": f"Sent: {command}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    asyncio.run(start_client())
    app.run(host="0.0.0.0", port=port)