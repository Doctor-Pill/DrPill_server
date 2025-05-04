# analyzers/face/recognition/visualizer.py
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


def save_face_clip(frames, bboxes, fps, identity, filename="face_clip.mp4"):
    if not frames:
        print("⚠️ 저장할 프레임이 없습니다.")
        return

    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    for frame, bbox in zip(frames, bboxes):
        annotated = frame.copy()
        if bbox:
            x, y, w, h = bbox
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(annotated, identity, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        out.write(annotated)

    out.release()
    print(f"✅ 얼굴 영상 클립 저장 완료: {filename}")
