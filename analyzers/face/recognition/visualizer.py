# analyzers/face/recognition/visualizer.py

import cv2

def draw_result(frame, label="Unknown"):
    """
    프레임의 좌측 상단에 라벨 텍스트를 출력
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    color = (0, 255, 0)

    cv2.putText(frame, label, (30, 50), font, font_scale, color, thickness)
    return frame
