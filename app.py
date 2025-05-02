# 📍 수정 추가 DRPILL_SERVER/app.py

import numpy as np
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

@socketio.on('connect', namespace='/client')
def on_connect():
    print("✅ 클라이언트 연결됨 (/client)")

@socketio.on('frame', namespace='/client')
def handle_frame(data):
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 확인용
    cv2.imwrite("received.jpg", frame)