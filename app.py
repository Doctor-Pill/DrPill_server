# 📍 DRPILL_SERVER/app.py

from flask import Flask, render_template
from flask_socketio import SocketIO
from src.config.settings import SECRET_KEY

# Flask 애플리케이션 생성
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# SocketIO 서버 생성 (CORS 허용)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ✅ 여기 추가! 서버 라우팅 설정
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/client')
def client():
    return render_template('client.html')
