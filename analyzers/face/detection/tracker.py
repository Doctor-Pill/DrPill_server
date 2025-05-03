# src/analyzers/face/detection/tracker.py

import time
import cv2

class FacePresenceTracker:
    def __init__(self, detector_backend="retinaface", threshold_sec=1.0):
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.detector_backend = detector_backend  # 사용하지 않지만 호환성 위해 유지
        self.threshold_sec = threshold_sec
        self.start_time = None
        self.last_frame_with_face = None

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        return faces

    def update(self, frame):
        faces = self.detect_faces(frame)
        has_face = len(faces) > 0

        now = time.time()

        if has_face:
            if self.start_time is None:
                self.start_time = now
            self.last_frame_with_face = frame
        else:
            self.start_time = None
            self.last_frame_with_face = None

        return has_face

    def is_face_persisted(self):
        if self.start_time is None:
            return False
        return time.time() - self.start_time >= self.threshold_sec

    def get_last_frame(self):
        return self.last_frame_with_face
