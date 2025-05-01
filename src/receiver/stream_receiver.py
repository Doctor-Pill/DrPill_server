import cv2
import threading

_receivers = {}

def _receive_stream(name: str, port: int, stop_flag):
    cap = cv2.VideoCapture(f"udp://@:{port}", cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print(f"❌ {name} 수신 실패 (포트 {port})")
        return

    print(f"📶 {name} 수신 시작 (UDP 포트 {port})")
    while not stop_flag["stop"]:
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ {name} 프레임 수신 실패")
            break

        cv2.imshow(f"{name} 수신", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"🧊 {name} 수신 종료됨")

def start_stream_receiver(name: str, port: int):
    if name in _receivers:
        return
    stop_flag = {"stop": False}
    thread = threading.Thread(target=_receive_stream, args=(name, port, stop_flag), daemon=True)
    _receivers[name] = (thread, stop_flag)
    thread.start()

def stop_stream_receiver(name: str):
    if name in _receivers:
        _, stop_flag = _receivers[name]
        stop_flag["stop"] = True
        del _receivers[name]
