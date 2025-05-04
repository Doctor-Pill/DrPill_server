# src/analyzers/face_recognition/identifier.py

from deepface import DeepFace

def identify_face(frame, db_path="data/patients", detector_backend="retinaface", threshold=0.3):
    """
    입력 프레임에서 얼굴을 감지하고, 등록된 얼굴과 충분히 유사한 경우에만 이름 반환
    """
    try:
        results = DeepFace.find(
            img_path=frame,
            db_path=db_path,
            detector_backend=detector_backend,
            enforce_detection=False
        )
        if len(results) > 0 and not results[0].empty:
            # 가장 가까운 얼굴 하나만 추출
            top_result = results[0].iloc[0]
            distance = top_result.get("distance", 1.0)

            if distance < threshold:
                identity_path = top_result['identity']
                return identity_path
            else:
                print(f"🟡 인식 실패: 거리({distance:.3f}) > 임계값({threshold})")
    except Exception as e:
        print("❌ 얼굴 인식 실패:", e)

    return None
