# 📍 DRPILL_SERVER/src/stream/receiver.py

import subprocess
from src.config.settings import FFPLAY_CMD

# 글로벌 변수로 ffplay 프로세스를 관리
ffplay_proc = None

# 영상 수신기 시작
def start_receiver():
    global ffplay_proc
    if ffplay_proc is None:
        print("▶️ ffplay 영상 수신 시작")
        ffplay_proc = subprocess.Popen(FFPLAY_CMD)
    else:
        print("ℹ️ ffplay 수신기가 이미 실행 중입니다.")

# 영상 수신기 중단
def stop_receiver():
    global ffplay_proc
    if ffplay_proc is not None:
        print("⏹️ ffplay 영상 수신 중단")
        ffplay_proc.terminate()
        ffplay_proc = None
    else:
        print("ℹ️ 수신기가 실행 중이지 않습니다.")
