import time
from deepface import DeepFace

class FacePresenceTracker:
    def __init__(self, threshold_sec=1.0, detector_backend='retinaface'):
        self.threshold_sec = threshold_sec
        self.start_time = None
        self.last_frame = None
        self.last_bbox = None
        self.detector_backend = detector_backend  # 문자열로만 보관

    def __str__(self):
        return (
            f"[FacePresenceTracker]\n"
            f"  threshold_sec: {self.threshold_sec}\n"
            f"  start_time: {self.start_time}\n"
            f"  last_bbox: {self.last_bbox}\n"
            f"  has_frame: {self.last_frame is not None}"
        )

    def update(self, frame):
        try:
            results = DeepFace.extract_faces(
                img_path=frame,
                detector_backend=self.detector_backend,
                enforce_detection=False
            )

            if results:
                face_info = results[0]
                region = face_info.get("facial_area", {})
                x, y, w, h = region.get("x"), region.get("y"), region.get("w"), region.get("h")

                if None not in (x, y, w, h):
                    self.last_bbox = (x, y, w, h)
                    self.last_frame = frame.copy()

                    if self.start_time is None:
                        self.start_time = time.time()
                else:
                    self._reset_tracking()
            else:
                self._reset_tracking()

        except Exception as e:
            print("❌ RetinaFace 감지 실패:", e)
            self._reset_tracking()

    def is_face_persisted(self):
        return self.start_time is not None and (time.time() - self.start_time) >= self.threshold_sec

    def get_last_frame(self):
        return self.last_frame

    def get_last_bbox(self):
        return self.last_bbox

    def reset(self):
        self._reset_tracking()

    def _reset_tracking(self):
        self.start_time = None
        self.last_frame = None
        self.last_bbox = None
