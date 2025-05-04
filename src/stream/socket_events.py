# 📍 src/stream/socket_events.py

from server.frame_handler import face_detection_thread


def register_socket_events(socketio):
    from flask_socketio import emit
    # from server.frame_handler import is_streaming_active
    from src.receiver.stream_receiver import start_stream_receiver, stop_stream_receiver

    @socketio.on('admin_command', namespace='/admin')
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

    @socketio.on('connect', namespace='/client')
    def handle_connect(auth=None):
        print("📡 클라이언트(WebSocket) 연결됨")

    @socketio.on('disconnect', namespace='/client')
    def handle_disconnect():
        print("📡 클라이언트(WebSocket) 연결 종료됨")