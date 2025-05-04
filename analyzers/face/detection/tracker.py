import cv2
import time

class FacePresenceTracker:
    def __init__(self, threshold_sec=1.0):
        self.threshold_sec = threshold_sec
        self.start_time = None
        self.last_frame = None
        self.last_bbox = None

    def __str__(self):
        return (
            f"[FacePresenceTracker]\n"
            f"  threshold_sec: {self.threshold_sec}\n"
            f"  start_time: {self.start_time}\n"
            f"  last_bbox: {self.last_bbox}\n"
            f"  has_frame: {self.last_frame is not None}"
        )

    def update(self, frame):
        # OpenCV 얼굴 감지기 (Haar Cascade 예시)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            self.last_frame = frame.copy()
            self.last_bbox = faces[0]  # 첫 번째 얼굴만 사용
            if self.start_time is None:
                self.start_time = time.time()
        else:
            self.start_time = None
            self.last_bbox = None

    def is_face_persisted(self):
        return self.start_time is not None and (time.time() - self.start_time) >= self.threshold_sec

    def get_last_frame(self):
        return self.last_frame

    def get_last_bbox(self):
        return self.last_bbox

    def reset(self):
        self.start_time = None
        self.last_frame = None
        self.last_bbox = None
