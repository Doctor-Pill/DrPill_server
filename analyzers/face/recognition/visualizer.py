# analyzers/face/recognition/visualizer.py
from deepface import DeepFace
import cv2

def draw_result(frame, label="Unknown", bbox=None):
    """
    프레임에 라벨과 바운딩 박스를 표시
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (0, 255, 0)

    if bbox is not None:
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10), font, font_scale, color, thickness)
    else:
        cv2.putText(frame, label, (30, 50), font, font_scale, color, thickness)

    return frame

def save_face_clip(frames, fps, identity="Unknown", filename="face_clip.mp4"):
    if not frames:
        print("⚠️ 저장할 프레임이 없습니다.")
        return

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    for frame in frames:
        try:
            results = DeepFace.extract_faces(
                img_path=frame[:, :, ::-1],  # BGR → RGB
                detector_backend="retinaface",
                enforce_detection=False
            )

            if results and 'facial_area' in results[0]:
                region = results[0]['facial_area']
                x, y, w, h = region.get("x"), region.get("y"), region.get("w"), region.get("h")
                if all(isinstance(v, int) and v > 0 for v in [x, y, w, h]):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, identity, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        except Exception as e:
            print("⚠️ save_face_clip 오류:", e)

        out.write(frame)

    out.release()
    print(f"✅ 얼굴 영상 클립 저장 완료: {filename}")
