import cv2
from src.config.settings import MJPEG_STREAM_URL

def gen_frames():
    cap = cv2.VideoCapture(MJPEG_STREAM_URL)
    if not cap.isOpened():
        print(f"❌ MJPEG 스트림 열기 실패: {MJPEG_STREAM_URL}")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        # 분석기 호출은 나중에 추가 (현재는 패스)

        # 스트리밍용 프레임 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
