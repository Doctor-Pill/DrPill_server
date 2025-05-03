# app.py

import numpy as np
import cv2
from flask import Flask, render_template
from flask_socketio import SocketIO
from src.config.settings import SECRET_KEY
from server.frame_handler import register_frame_handler

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

register_frame_handler(socketio)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/client')
def client():
    return render_template('client.html')

@socketio.on('connect', namespace='/client')
def on_connect():
    print("✅ 클라이언트 연결됨 (/client)")
