from deepface import DeepFace

# 모델별 추천 threshold
THRESHOLDS = {
    "VGG-Face": 0.4,
    "Facenet": 10,
    "Facenet512": 0.9,
    "ArcFace": 0.68,
    "Dlib": 0.6,
    "SFace": 0.593
}

def identify_face(frame, db_path="data/patients", detector_backend="retinaface", model_name="Facenet"):
    """
    입력 프레임에서 얼굴을 감지하고, 등록된 얼굴과 충분히 유사한 경우에만 이름 반환
    """
    threshold = THRESHOLDS.get(model_name, 0.5)

    try:
        results = DeepFace.find(
            img_path=frame,
            db_path=db_path,
            detector_backend=detector_backend,
            model_name=model_name,
            enforce_detection=False
        )

        if len(results) > 0 and not results[0].empty:
            top_result = results[0].iloc[0]
            distance = top_result.get("distance", 1.0)

            if distance < threshold:
                identity_path = top_result['identity']
                print(f"🟢 인식 성공: 거리({distance:.3f}) <= 임계값({threshold})")
                return identity_path.split("/")[-1].split("_")[0]
            else:
                print(f"🟡 인식 실패: 거리({distance:.3f}) > 임계값({threshold})")
    except Exception as e:
        print("❌ 얼굴 인식 실패:", e)

    return None
