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
