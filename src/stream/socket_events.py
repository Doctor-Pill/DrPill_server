# 📍 수정 후 src/stream/socket_events.py

from flask_socketio import emit
from app import socketio
from src.stream.receiver import start_receiver, stop_receiver

# 클라이언트가 소켓에 연결될 때
@socketio.on('connect')
def handle_connect(auth):  # ✅ 인자 하나 받아야 함
    log_message("📡 클라이언트가 WebSocket에 연결됨")

# 클라이언트에서 'start_video' 이벤트 수신 시 처리
@socketio.on('start_video')
def handle_start_video():
    log_message("▶️ start_video 수신됨 → 모든 클라이언트에 브로드캐스트")
    emit('start_video', broadcast=True)

# 클라이언트에서 'stop_video' 이벤트 수신 시 처리
@socketio.on('stop_video')
def handle_stop_video():
    log_message("⏹️ stop_video 수신됨 → 모든 클라이언트에 브로드캐스트")
    emit('stop_video', broadcast=True)

# 클라이언트에서 영상 프레임 전송 시
@socketio.on('video_frame')
def handle_video_frame(data):
    emit('video_frame', data, broadcast=True)

# WebSocket 에러 핸들링
@socketio.on_error_default
def default_error_handler(e):
    import traceback
    print("🔥 [SocketIO 서버 오류 발생]", e)
    traceback.print_exc()

# 로그 메세지를 소켓으로 전송
def log_message(msg):
    print(msg)
    emit('log_message', msg, broadcast=True)  # ✅ socketio.emit이 아니라 emit!
