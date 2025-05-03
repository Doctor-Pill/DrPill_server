# # 📍 src/stream/socket_events.py

import threading
from flask_socketio import emit
from app import socketio
from src.receiver.stream_receiver import start_stream_receiver, stop_stream_receiver
from server.frame_handler import is_streaming_active

@socketio.on('admin_command', namespace='/admin')  # ✅ 올바름
def handle_admin_command(data):
    command = data.get('command')
    print(f"➡️ [Admin] 서버가 엣지로 명령 전송: {command}")
    emit('edge_command', {"command": command}, broadcast=True)

    if command == "stop_streaming":
        stop_stream_receiver("USB")
        stop_stream_receiver("PICAM")

@socketio.on('usb_streaming_ready', namespace='/client')
def handle_usb_ready():
    print("📥 엣지에서 USB 송신 준비 완료 알림 수신")
    start_stream_receiver("USB", 5001)

@socketio.on('picam_streaming_ready', namespace='/client')
def handle_picam_ready():
    print("📥 엣지에서 PiCam 송신 준비 완료 알림 수신")
    start_stream_receiver("PICAM", 5002)


# 클라이언트가 소켓에 연결될 때
@socketio.on('connect', namespace='/client')
def handle_connect(auth=None):  # auth=None 추가 (경고 제거)
    print("📡 클라이언트(WebSocket) 연결됨")

# 엣지가 서버로부터 연결 끊겼을 때
@socketio.on('disconnect', namespace='/client')
def handle_disconnect():
    print("📡 클라이언트(WebSocket) 연결 종료됨")

@socketio.on('start_face_detection', namespace='/admin')
def start_face_detection():
    global identity_found, face_detection_active

    if not is_streaming_active():
        print("🚫 감지 실패: 카메라 스트리밍 중이 아님")
        emit('log_message', "🚫 감지 시작 실패: 현재 영상이 수신되지 않고 있습니다", namespace='/admin')
        return

    identity_found = False
    face_detection_active = True
    print("🟢 얼굴 감지 시작됨")
    emit('log_message', "🟢 얼굴 감지 시작됨", namespace='/admin')


# # 로그 메시지 브로드캐스트용 (선택)
# def log_message(msg):
#     print(msg)
#     socketio.emit('log_message', msg, broadcast=True)

