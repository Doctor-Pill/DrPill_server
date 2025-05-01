# # 📍 src/stream/socket_events.py

# from flask_socketio import emit
# from app import socketio

# # 엣지로 명령 보내기 (핵심 추가)
# @socketio.on('admin_command')
# def handle_admin_command(data):
#     command = data.get('command')
#     print(f"➡️ [Admin] 서버가 엣지로 명령 전송: {command}")
#     emit('edge_command', {"command": command}, broadcast=True)

# 📍 src/stream/socket_events.py

from flask_socketio import emit
from app import socketio
from src.receiver.stream_receiver import start_stream_receiver, stop_stream_receiver

@socketio.on('admin_command')
def handle_admin_command(data):
    command = data.get('command')
    print(f"➡️ [Admin] 서버가 엣지로 명령 전송: {command}")

    # 🎯 서버 수신도 함께 제어
    if command == "start_usb_streaming":
        start_stream_receiver("USB", 5001)
    elif command == "start_picam_streaming":
        start_stream_receiver("PICAM", 5002)
    elif command == "stop_streaming":
        stop_stream_receiver("USB")
        stop_stream_receiver("PICAM")

    emit('edge_command', {"command": command}, broadcast=True)

# 클라이언트가 소켓에 연결될 때
@socketio.on('connect')
def handle_connect(auth=None):  # auth=None 추가 (경고 제거)
    print("📡 클라이언트(WebSocket) 연결됨")

# 엣지가 서버로부터 연결 끊겼을 때
@socketio.on('disconnect')
def handle_disconnect():
    print("📡 클라이언트(WebSocket) 연결 종료됨")

# 로그 메시지 브로드캐스트용 (선택)
def log_message(msg):
    print(msg)
    socketio.emit('log_message', msg, broadcast=True)
