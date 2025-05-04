import time
from collections import deque
import numpy as np
import cv2
import threading
from flask_socketio import emit

from app import socketio
from analyzers.face.detection.tracker import FacePresenceTracker
from analyzers.face.recognition.identifier import identify_face
from analyzers.face.recognition.visualizer import draw_result

# ----------------------------- 상태 변수 ----------------------------- #
face_tracker = FacePresenceTracker(threshold_sec=1.0)
identity_found = False
face_detection_active = False

latest_frame = None
frame_lock = threading.Lock()

# ----------------------------- 영상 저장 관련 ----------------------------- #
video_seconds = 6         # ✅ 얼굴 인식 성공 전 몇 초를 저장할지
video_fps = 10            # ✅ 엣지에서 보낸다고 가정한 fps
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
    global identity_found, face_detection_active, latest_frame

    while face_detection_active:
        with frame_lock:
            if latest_frame is None:
                continue
            frame_copy = latest_frame.copy()

        face_tracker.update(frame_copy)
        print(face_tracker)

        if face_tracker.is_face_persisted():
            last_frame = face_tracker.get_last_frame()
            bbox = face_tracker.get_last_bbox()

            # ✅ 감지되었으니 로그 및 영상 저장 먼저
            socketio.emit('log_message', f'DB에서 얼굴 찾는 중...', namespace='/admin')
            save_face_clip(
                frames=list(frame_queue),
                fps=video_fps,
                bbox=bbox,
                identity="Identifying...",
                filename="face_clip.mp4"
            )

            # ✅ 실제 얼굴 인식 수행
            identity_path = identify_face(last_frame)
            print("identity_path", identity_path)

            if identity_path:
                identity_found = True
                result_frame = draw_result(last_frame, label=identity_path, bbox=bbox)
                cv2.imwrite("final_identified.jpg", result_frame)

                socketio.emit('identified', {'user': identity_path}, namespace='/client')
                socketio.emit('log_message', f'✅ 얼굴 인식 완료: {identity_path}', namespace='/admin')
                face_tracker.reset()
                stop_face_detection()
                break
            else:
                socketio.emit('log_message', "❌ 얼굴은 있었지만 식별 실패", namespace='/admin')
                face_tracker.reset()
                stop_face_detection()
                break
        else:
            socketio.emit('log_message', "⏳ 얼굴 감지 중...", namespace='/admin')

# ----------------------------- 얼굴 인식 시작 ----------------------------- #
@socketio.on('start_face_detection', namespace='/admin')
def start_face_detection():
    global face_detection_active, identity_found
    face_detection_active = True
    identity_found = False

    socketio.emit('log_message', "🟢 얼굴 인식 시작됨 → 엣지에 카메라 요청", namespace='/admin')
    socketio.emit('edge_command', {"command": "start_usb_streaming"}, namespace='/admin')

    threading.Thread(target=face_detection_thread, daemon=True).start()

# ----------------------------- 얼굴 인식 중단 ----------------------------- #
@socketio.on('stop_face_detection', namespace='/admin')
def stop_face_detection():
    global face_detection_active
    face_detection_active = False

    socketio.emit('edge_command', {"command": "stop_streaming"}, namespace='/admin')
    socketio.emit('log_message', "🔴 얼굴 감지 중단됨 → 엣지에 스트리밍 중단 요청", namespace='/admin')

# ----------------------------- 영상 저장 함수 ----------------------------- #
def save_face_clip(frames, fps, bbox, identity, filename="face_clip.mp4"):
    if not frames:
        print("⚠️ 저장할 프레임이 없습니다.")
        return

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    for frame in frames:
        annotated = draw_result(frame.copy(), label=identity, bbox=bbox)
        out.write(annotated)

    out.release()
    print(f"✅ 얼굴 영상 클립 저장됨: {filename}")
