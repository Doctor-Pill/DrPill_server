from flask import render_template, Response
from app import app
from src.stream.analyzer_runner import gen_frames  # 스트림 프레임 생성기 불러오기

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/client')
def client_page():
    return render_template('client.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
