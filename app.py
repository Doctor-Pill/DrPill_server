# 📍 수정 추가 DRPILL_SERVER/app.py

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from src.config.settings import SECRET_KEY
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ✅ 기본 라우트들
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/client')
def client():
    return render_template('client.html')

# ✅ 스트림 라우트 추가
@app.route('/stream')
def stream():
    """
    UDP 스트림을 받아서 MJPEG로 브라우저에 중계
    """
    def generate():
        cap = cv2.VideoCapture('udp://0.0.0.0:5000', cv2.CAP_FFMPEG)

        while True:
            success, frame = cap.read()
            if not success:
                continue

            # 프레임을 JPEG 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # MJPEG 포맷으로 반환
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
