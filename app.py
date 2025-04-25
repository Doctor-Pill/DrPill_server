from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import threading
import time
import signal
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ▶ 전역 변수
admin_browser_proc = None

# ▶ 라우트
@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# ▶ WebSocket 이벤트
@socketio.on('connect')
def handle_connect():
    log_message("📡 클라이언트가 소켓에 연결됨")

@socketio.on('start_video')
def handle_start_video():
    log_message("▶️ 클라이언트 영상 시작")
    emit('start_video', broadcast=True)

@socketio.on('stop_video')
def handle_stop_video():
    log_message("⏹️ 클라이언트 영상 중단")
    emit('stop_video', broadcast=True)

@socketio.on('video_frame')
def handle_video_frame(data):
    emit('video_frame', data, broadcast=True)

# ▶ 에러 핸들러
@socketio.on_error_default
def default_error_handler(e):
    import traceback
    print("🔥 [SocketIO 서버 오류 발생]", e)
    traceback.print_exc()


# ▶ 로깅 함수
def log_message(msg):
    print(msg)
    socketio.emit('log_message', msg, broadcast=True)

# ▶ 라즈베리파이 브라우저 실행
def open_browser_on_pi():
    try:
        subprocess.run([
            "ssh", "drpill@192.168.0.20",
            "DISPLAY=:0 chromium-browser --noerrdialogs --use-fake-ui-for-media-stream --kiosk http://192.168.0.10:5000/client"
        ], check=True)
        print("🚀 라즈베리파이 브라우저 실행됨")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 라즈베리파이 브라우저 실행 실패: {e}")

# ▶ 라즈베리파이 브라우저 종료
def close_browser_on_pi():
    try:
        subprocess.run([
            "ssh", "drpill@192.168.0.20",
            "pkill -9 -f 'chromium.*kiosk'"
        ], check=True)
        print("🛑 라즈베리파이 브라우저 강제 종료됨")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 라즈베리파이 브라우저 종료 실패: {e}")

# ▶ 서버 시작 시 브라우저 자동 실행
def startup():
    global admin_browser_proc
    time.sleep(1)

    try:
        admin_browser_proc = subprocess.Popen([
            "google-chrome",
            "--new-window",
            "--noerrdialogs",
            "http://localhost:5000/admin"
        ])
        print("🚀 워크스테이션 브라우저 실행됨")
    except Exception as e:
        print(f"⚠️ 워크스테이션 브라우저 실행 실패: {e}")

    open_browser_on_pi()

# ▶ 서버 종료 시 브라우저 정리
def cleanup(*args):
    global admin_browser_proc
    print("\n🧹 서버 종료 중... 브라우저 정리 중...")

    if admin_browser_proc:
        admin_browser_proc.terminate()
        print("🛑 워크스테이션 브라우저 종료 시도 (.terminate())")
        subprocess.run(["pkill", "-f", "http://localhost:5000/admin"], stdout=subprocess.DEVNULL)
        print("🧨 워크스테이션 브라우저 강제 종료 (pkilled)")

    close_browser_on_pi()
    sys.exit(0)

# ▶ 메인 실행
if __name__ == '__main__':
    threading.Thread(target=startup).start()
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    socketio.run(app, host='0.0.0.0', port=5000)
