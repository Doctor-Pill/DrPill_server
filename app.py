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