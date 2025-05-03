# server/frame_handler.py

from flask_socketio import emit
import numpy as np
import cv2
import threading

from analyzers.face.detection.tracker import FacePresenceTracker
from analyzers.face.recognition.identifier import identify_face
from analyzers.face.recognition.visualizer import draw_result

# 전역 상태 변수
face_tracker = FacePresenceTracker(threshold_sec=1.0)
identity_found = False
face_detection_active = False
streaming_active = False
monitor_started = False  # ✅ 중복 방지

def is_streaming_active():
    return streaming_active

# 🔽 스트리밍 중단 시 감지 종료 처리
def stop_face_detection_due_to_stream_loss():
    global face_detection_active
    face_detection_active = False

    try:
        from app import socketio
        socketio.emit('log_message', "🛑 스트리밍 중단으로 얼굴 감지 중단됨", namespace='/admin')
    except Exception as e:
        print("❌ 스트리밍 중단 알림 실패:", e)

# 🔽 스트리밍 감시 스레드 실행
def monitor_streaming():
    global streaming_active, face_detection_active

    def check_loop():
        while True:
            if face_detection_active:
                streaming_active = False  # 🔄 매 2초마다 초기화
                threading.Event().wait(2.0)
                if not streaming_active:
                    stop_face_detection_due_to_stream_loss()
            else:
                threading.Event().wait(2.0)

    threading.Thread(target=check_loop, daemon=True).start()

# 🔽 등록 함수
def register_frame_handler(socketio):
    global monitor_started

    @socketio.on('frame', namespace='/client')
    def handle_frame(data):
        global identity_found, face_detection_active, streaming_active

        streaming_active = True  # 프레임 수신 중
        if not face_detection_active or identity_found:
            return

        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        face_tracker.update(frame)

        if face_tracker.is_face_persisted():
            last_frame = face_tracker.get_last_frame()
            identity = identify_face(last_frame)

            if identity:
                identity_found = True
                result_frame = draw_result(last_frame, label=identity)
                cv2.imwrite("final_identified.jpg", result_frame)

                emit('identified', {'user': identity}, namespace='/client')
                emit('log_message', f'✅ 얼굴 인식 완료: {identity}', namespace='/admin')
            else:
                emit('log_message', "❌ 얼굴은 있었지만 식별 실패", namespace='/admin')
        else:
            emit('log_message', "⏳ 얼굴 감지 중...", namespace='/admin')

    @socketio.on('start_face_detection', namespace='/admin')
    def start_face_detection():
        global identity_found, face_detection_active
        identity_found = False
        face_detection_active = True
        emit('log_message', "🟢 얼굴 감지 시작됨", namespace='/admin')

    @socketio.on('stop_face_detection', namespace='/admin')
    def stop_face_detection():
        global face_detection_active
        face_detection_active = False
        emit('log_message', "🔴 얼굴 감지 중단됨", namespace='/admin')

    # ✅ 스트리밍 모니터는 최초 한 번만 실행
    if not monitor_started:
        monitor_streaming()
        monitor_started = True
