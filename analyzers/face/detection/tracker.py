from deepface import DeepFace

class FacePresenceTracker:
    def __init__(self, detector_backend='retinaface'):
        self.last_frame = None
        self.last_bbox = None
        self.detector_backend = detector_backend

    def update(self, frame):
        try:
            results = DeepFace.extract_faces(
                img_path=frame[:, :, ::-1],
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            if results and isinstance(results[0], dict):
                region = results[0].get("facial_area", {})
                confidence = results[0].get("confidence", 0)
                x, y, w, h = region.get("x"), region.get("y"), region.get("w"), region.get("h")
                if confidence > 0 and all(isinstance(v, int) and v > 0 for v in [x, y, w, h]):
                    self.last_bbox = (x, y, w, h)
                    self.last_frame = frame.copy()
                else:
                    self.reset()
            else:
                self.reset()
        except Exception as e:
            print("❌ 얼굴 감지 실패:", e)
            self.reset()

    def get_last_frame(self):
        return self.last_frame

    def get_last_bbox(self):
        return self.last_bbox

    def reset(self):
        self.last_frame = None
        self.last_bbox = None
