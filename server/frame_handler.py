import time
from collections import deque
import numpy as np
import cv2
import threading
from flask_socketio import emit

from app import socketio
from analyzers.face.detection.tracker import FacePresenceTracker
from analyzers.face.recognition.identifier import identify_face_from_bbox
from analyzers.face.recognition.visualizer import draw_result

# ----------------------------- 상태 변수 ----------------------------- #
face_tracker = FacePresenceTracker()
face_detection_active = False
latest_frame = None
frame_lock = threading.Lock()

video_seconds = 6
video_fps = 10
frame_queue = deque(maxlen=video_seconds * video_fps)

# ----------------------------- 프레임 수신 ----------------------------- #
@socketio.on('frame', namespace='/client')
def receive_frame(data):
    global latest_frame
    nparr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        print("❌ 프레임 디코딩 실패")
        return

    with frame_lock:
        latest_frame = frame
        frame_queue.append(frame.copy())

# ----------------------------- 얼굴 인식 스레드 ----------------------------- #
def face_detection_thread():
    global face_detection_active

    socketio.emit('log_message', "🟡 얼굴 인식 시작됨", namespace='/admin')

    while face_detection_active:
        with frame_lock:
            if latest_frame is None:
                continue
            frame_copy = latest_frame.copy()

        face_tracker.update(frame_copy)
        bbox = face_tracker.get_last_bbox()
        frame = face_tracker.get_last_frame()

        if bbox is None or frame is None:
            continue

        socketio.emit('log_message', "🔍 얼굴 감지됨 → DB에서 얼굴 인식 시도 중", namespace='/admin')

        identity = identify_face_from_bbox(frame, bbox)

        print(frame, bbox, identity)
        result_frame = draw_result(frame.copy(), label=identity, bbox=bbox)
        cv2.imwrite("final_identified.jpg", result_frame)
        if identity:
            socketio.emit('log_message', f"✅ 얼굴 인식 완료: {identity}", namespace='/admin')
        else:
            socketio.emit('log_message', "❌ 등록되지 않은 얼굴입니다", namespace='/admin')

        stop_face_detection()
        break

# ----------------------------- 시작 / 중단 이벤트 ----------------------------- #
@socketio.on('start_face_detection', namespace='/admin')
def start_face_detection():
    global face_detection_active
    face_detection_active = True
    socketio.emit('log_message', "🟢 얼굴 인식 프로세스 시작", namespace='/admin')
    socketio.emit('edge_command', {"command": "start_usb_streaming"}, namespace='/admin')
    threading.Thread(target=face_detection_thread, daemon=True).start()

@socketio.on('stop_face_detection', namespace='/admin')
def stop_face_detection():
    global face_detection_active
    face_detection_active = False
    socketio.emit('edge_command', {"command": "stop_streaming"}, namespace='/admin')
    socketio.emit('log_message', "🔴 얼굴 인식 프로세스 중단", namespace='/admin')
