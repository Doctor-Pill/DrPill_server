# app.py

import numpy as np
import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO
from src.config.settings import SECRET_KEY

# Flask와 socketio 객체를 초기화
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# 기본 라우트
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/edge_base')
def edge_base():
    return render_template('edge_base.html')

@app.route('/face_alert')
def face_alert():
    return render_template('face_alert.html')

@app.route('/face_waiting')
def face_waiting():
    return render_template('face_waiting.html')

@app.route('/face_success')
def face_success():
    return render_template('face_success.html')

@app.route('/face_fail')
def face_fail():
    return render_template('face_fail.html')

@app.route('/home')
def home():
    return render_template('home.html')


@socketio.on('connect', namespace='/client')
def on_connect():
    print("✅ 클라이언트 연결됨 (/client)")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
