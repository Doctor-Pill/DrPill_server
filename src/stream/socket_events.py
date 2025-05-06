# 포함된 socket_events.py

from flask import request
from flask_socketio import emit
from server.frame_handler import face_detection_thread

servo_state = {"enabled": False}  # 전역 상태 저장 (선택)

def register_socket_events(socketio):
    from src.receiver.stream_receiver import start_stream_receiver, stop_stream_receiver

    @socketio.on('admin_command', namespace='/admin')
    def handle_admin_command(data):
        command = data.get('command')
        print(f"➡️ [Admin] 서버가 엣지로 명령 전송: {command}")

        if command.startswith("go:"):
            path = command[3:] or "/home"
            print(f"🔁 페이지 이동 명령: {path}")
            emit("redirect", {"url": path}, namespace='/', broadcast=True)
        else:
            emit("edge_command", {"command": command}, namespace='/', broadcast=True)

        if command == "stop_streaming":
            stop_stream_receiver("USB")
            stop_stream_receiver("PICAM")


    @socketio.on('call_patient', namespace='/admin')
    def on_call_patient():
        print("📣 모든 클라이언트 /ready로")
        emit('redirect', {'url': '/ready'}, broadcast=True)

    @socketio.on('ready_ack')
    def on_ready_ack():
        print(f"✅ 클라이언트 도착 확인: {request.sid}")
        emit('redirect', {'url': '/face'}, to=request.sid)

    @socketio.on('toggle_servo', namespace='/admin')
    def on_toggle_servo(data):
        enabled = data.get("enabled", False)
        servo_state["enabled"] = enabled
        print(f"🔧 서보모터 활성화 여부: {enabled}")
        emit("toggle_servo", {"enabled": enabled}, broadcast=True)  # → 엣지에 전달


    @socketio.on('usb_streaming_ready')
    def handle_usb_ready():
        print("📥 엣지에서 USB 송신 준비 완료 알림 수신")
        start_stream_receiver("USB", 5001)

    @socketio.on('picam_streaming_ready')
    def handle_picam_ready():
        print("📥 엣지에서 PiCam 송신 준비 완료 알림 수신")
        start_stream_receiver("PICAM", 5002)

    @socketio.on('connect')
    def handle_connect(auth=None):
        print("📱 클라이언트(WebSocket) 연결됨")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("📱 클라이언트(WebSocket) 연결 종료됨")
