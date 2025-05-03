# 📄 app.py 또는 route_handler.py

from flask import render_template, Response
from app import app, socketio  # ✅ socketio 추가
from src.stream.analyzer_runner import gen_frames
from server.frame_handler import enable_face_detection  # ✅ 얼굴 인식 활성화 함수

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/client')
def client_page():
    return render_template('client.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('start_face_detection')  # ✅ 클라이언트가 이 명령을 보낼 때 실행됨
def on_start_face_detection():
    enable_face_detection()
    print("🧠 얼굴 인식 시작 요청 수신됨")
    socketio.emit('log_message', '🧠 얼굴 인식 시작됨 (프레임 수신 시작)')
