# src/analyzers/face_recognition/identifier.py

from deepface import DeepFace

def identify_face(frame, db_path="data/patients", detector_backend="retinaface"):
    """
    입력 프레임에서 얼굴을 감지하고, 등록된 얼굴과 매칭된 사람의 이름 반환
    """
    try:
        results = DeepFace.find(
            img_path=frame,
            db_path=db_path,
            detector_backend=detector_backend,
            enforce_detection=False
        )
        if len(results) > 0 and not results[0].empty:
            identity_path = results[0]['identity'].values[0]
            return identity_path.split("/")[-1].split(".")[0]  # 예: "user01"
    except Exception as e:
        print("❌ 얼굴 인식 실패:", e)
    return None
