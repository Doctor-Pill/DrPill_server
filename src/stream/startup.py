# 📍 DRPILL_SERVER/src/stream/startup.py

import subprocess
import time
from src.config.settings import ADMIN_BROWSER_CMD, RASPBERRY_PI_IP, RASPBERRY_BROWSER_CMD, RASPBERRY_CLOSE_CMD

admin_browser_proc = None  # 서버 쪽 브라우저 프로세스 저장용

def open_admin_browser():
    """
    워크스테이션(서버)에서 admin.html 띄우기
    """
    global admin_browser_proc
    try:
        admin_browser_proc = subprocess.Popen(ADMIN_BROWSER_CMD)
        print("🚀 워크스테이션 관리자 브라우저 실행됨")
    except Exception as e:
        print(f"⚠️ 워크스테이션 브라우저 실행 실패: {e}")

def close_admin_browser():
    """
    워크스테이션(서버)에서 admin.html 띄운 브라우저 종료
    """
    global admin_browser_proc
    if admin_browser_proc:
        try:
            admin_browser_proc.terminate()
            subprocess.run(["pkill", "-f", "http://localhost:5000/admin"], stdout=subprocess.DEVNULL)
            print("🛑 워크스테이션 브라우저 종료 완료?")
        except Exception as e:
            print(f"⚠️ 워크스테이션 브라우저 종료 실패: {e}")

def open_client_browser_on_pi():
    """
    SSH로 라즈베리파이에 접속해서 client.html 띄우기 (명령어를 백그라운드 실행)
    """
    try:
        subprocess.run([
            "ssh", f"drpill@{RASPBERRY_PI_IP}",
            f"{RASPBERRY_BROWSER_CMD} &"
        ], check=True)
        print("🚀 라즈베리파이 브라우저 실행 (백그라운드)")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 라즈베리파이 브라우저 실행 실패: {e}")

def close_client_browser_on_pi():
    """
    SSH로 라즈베리파이에 접속해서 브라우저 종료
    """
    try:
        subprocess.run([
            "ssh", f"drpill@{RASPBERRY_PI_IP}",
            RASPBERRY_CLOSE_CMD
        ], check=True)
        print("🛑 라즈베리파이 브라우저 종료 완료")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 라즈베리파이 브라우저 종료 실패: {e}")

def start_edge_main_on_pi():
    """
    라즈베리파이 내부에서 ~/DrPill_edge/main.py 실행
    (가상환경 python으로 완전히 detached하게 실행)
    """
    try:
        subprocess.Popen([
            "ssh", f"drpill@{RASPBERRY_PI_IP}",
            "nohup ~/DrPill_edge/.venv/bin/python ~/DrPill_edge/main.py > /dev/null 2>&1 &"
        ])
        print("🚀 라즈베리파이에서 main.py 실행 명령 전송 완료 (비동기)")
    except Exception as e:
        print(f"⚠️ 라즈베리파이 main.py 실행 실패: {e}")

def reset_camera_on_pi():
    try:
        subprocess.run([
            "ssh", f"drpill@{RASPBERRY_PI_IP}",
            "pkill -f 'libcamera' || true && fuser -k /dev/video0 || true"
        ], check=True)
        print("🧹 라즈베리파이 카메라 리셋 완료")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 라즈베리파이 카메라 리셋 실패: {e}")

def startup():
    """
    서버 시작 시 브라우저 및 엣지 자동 실행
    """
    # time.sleep(1)
    # reset_camera_on_pi()  # 🔥 추가!
    open_admin_browser()
    # start_edge_main_on_pi()
    # open_client_browser_on_pi()

def cleanup():
    """
    서버 종료 시 브라우저 자동 정리
    """
    close_admin_browser()
    # close_client_browser_on_pi()
    # reset_camera_on_pi()  # 🔥 추가!

