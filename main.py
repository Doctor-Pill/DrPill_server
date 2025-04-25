# 📍 DRPILL_SERVER/main.py

import signal
import sys
import threading
from app import app, socketio
from src.stream.startup import startup, cleanup
from src.stream import socket_events  # WebSocket 이벤트 등록용

if __name__ == "__main__":
    # 서버 시작 시 브라우저 띄우기
    threading.Thread(target=startup).start()

    # 서버 종료 시 브라우저 종료
    signal.signal(signal.SIGINT, lambda sig, frame: (cleanup(), sys.exit(0)))
    signal.signal(signal.SIGTERM, lambda sig, frame: (cleanup(), sys.exit(0)))

    socketio.run(app, host='0.0.0.0', port=5000)
