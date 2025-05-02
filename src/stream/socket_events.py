# # 📍 src/stream/socket_events.py

import threading
from flask_socketio import emit
from app import socketio
from src.receiver.stream_receiver import start_stream_receiver, stop_stream_receiver

@socketio.on('admin_command')
def handle_admin_command(data):
    command = data.get('command')
    print(f"➡️ [Admin] 서버가 엣지로 명령 전송: {command}")
    emit('edge_command', {"command": command}, broadcast=True)

    if command == "stop_streaming":
        stop_stream_receiver("USB")
        stop_stream_receiver("PICAM")

@socketio.on('usb_streaming_ready')
def handle_usb_ready():
    print("📥 엣지에서 USB 송신 준비 완료 알림 수신")
    start_stream_receiver("USB", 5001)

@socketio.on('picam_streaming_ready')
def handle_picam_ready():
    print("📥 엣지에서 PiCam 송신 준비 완료 알림 수신")
    start_stream_receiver("PICAM", 5002)


# 클라이언트가 소켓에 연결될 때
@socketio.on('connect')
def handle_connect(auth=None):  # auth=None 추가 (경고 제거)
    print("📡 클라이언트(WebSocket) 연결됨")

# 엣지가 서버로부터 연결 끊겼을 때
@socketio.on('disconnect')
def handle_disconnect():
    print("📡 클라이언트(WebSocket) 연결 종료됨")

# # 로그 메시지 브로드캐스트용 (선택)
# def log_message(msg):
#     print(msg)
#     socketio.emit('log_message', msg, broadcast=True)

