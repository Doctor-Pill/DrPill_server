from flask_socketio import emit
import numpy as np
import cv2
import threading

from app import socketio
from analyzers.face.detection.tracker import FacePresenceTracker
from analyzers.face.recognition.identifier import identify_face
from analyzers.face.recognition.visualizer import draw_result

# 상태 변수
face_tracker = FacePresenceTracker(threshold_sec=1.0)
identity_found = False
face_detection_active = False

latest_frame = None
frame_lock = threading.Lock()

# 🔽 엣지에서 전송된 프레임 수신
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


# 🔽 얼굴 인식 스레드
def face_detection_thread():
    global identity_found, face_detection_active, latest_frame

    while face_detection_active:
        with frame_lock:
            if latest_frame is None:
                continue
            frame_copy = latest_frame.copy()

        print("face_detection_thread")  # ✅ 수신 로그 추가
        face_tracker.update(frame_copy)

        if face_tracker.is_face_persisted():
            last_frame = face_tracker.get_last_frame()
            identity = identify_face(last_frame)

            if identity:
                identity_found = True
                result_frame = draw_result(last_frame, label=identity)
                cv2.imwrite("final_identified.jpg", result_frame)
                socketio.emit('identified', {'user': identity}, namespace='/client')
                socketio.emit('log_message', f'✅ 얼굴 인식 완료: {identity}', namespace='/admin')
                stop_face_detection()
                break
            else:
                socketio.emit('log_message', "❌ 얼굴은 있었지만 식별 실패", namespace='/admin')
                stop_face_detection()
                break
        else:
            socketio.emit('log_message', "⏳ 얼굴 감지 중...", namespace='/admin')

# 🔽 얼굴 인식 시작
@socketio.on('start_face_detection', namespace='/admin')
def start_face_detection():
    global face_detection_active, identity_found
    face_detection_active = True
    identity_found = False

    socketio.emit('log_message', "🟢 얼굴 인식 시작됨 → 엣지에 카메라 요청", namespace='/admin')
    socketio.emit('edge_command', {"command": "start_usb_streaming"}, namespace='/admin')

    threading.Thread(target=face_detection_thread, daemon=True).start()

# 🔽 얼굴 인식 중단
@socketio.on('stop_face_detection', namespace='/admin')
def stop_face_detection():
    global face_detection_active
    face_detection_active = False

    socketio.emit('edge_command', {"command": "stop_streaming"}, namespace='/admin')
    socketio.emit('log_message', "🔴 얼굴 감지 중단됨 → 엣지에 스트리밍 중단 요청", namespace='/admin')
