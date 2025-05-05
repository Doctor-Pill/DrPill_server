from deepface import DeepFace
import cv2

def identify_face_from_bbox(frame, bbox):
    try:
        height, width = frame.shape[:2]
        x, y, w, h = bbox
        x = max(0, x)
        y = max(0, y)
        x2 = min(width, x + w)
        y2 = min(height, y + h)
        face_crop = frame[y:y2, x:x2]

        # print("📐 얼굴 크기:", face_crop.shape)
        # cv2.imwrite("debug_face_crop.jpg", face_crop)

        face_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)

        result = DeepFace.find(
            img_path=face_rgb,
            db_path="data/patients/face",
            model_name="Facenet512",
            detector_backend="retinaface",
            enforce_detection=False
        )

        print("🔍 인식 결과:", result)

        if len(result) > 0 and len(result[0]) > 0:
            identity_path = result[0].iloc[0]["identity"]
            return identity_path.split("/")[-1].split(".")[0]
    except Exception as e:
        print("❌ 얼굴 인식 오류:", e)
    return None
