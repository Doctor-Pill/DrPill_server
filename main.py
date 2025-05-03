# main.py

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import signal
import threading
from app import app, socketio
from src.stream.startup import startup, cleanup
from src.stream import socket_events  # WebSocket 이벤트 등록

if __name__ == "__main__":
    threading.Thread(target=startup).start()

    signal.signal(signal.SIGINT, lambda sig, frame: (cleanup(), sys.exit(0)))
    signal.signal(signal.SIGTERM, lambda sig, frame: (cleanup(), sys.exit(0)))

    socketio.run(app, host='0.0.0.0', port=5000)
