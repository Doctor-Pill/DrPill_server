# main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import signal
import threading
from app import app, socketio
from src.stream.startup import startup, cleanup
from src.stream.socket_events import register_socket_events  # ✅ 함수 임포트

if __name__ == "__main__":
    register_socket_events(socketio)  # ✅ 명시적으로 소켓 이벤트 등록
    threading.Thread(target=startup).start()

    signal.signal(signal.SIGINT, lambda sig, frame: (cleanup(), sys.exit(0)))
    signal.signal(signal.SIGTERM, lambda sig, frame: (cleanup(), sys.exit(0)))

    socketio.run(app, host='0.0.0.0', port=5000)