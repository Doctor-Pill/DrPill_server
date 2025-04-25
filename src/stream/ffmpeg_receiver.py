import subprocess

def start_receiving():
    """
    UDP로 들어오는 스트림을 받아서 화면에 띄운다.
    """

    command = [
        'ffplay',
        '-fflags', 'nobuffer',        # 지연 최소화
        '-flags', 'low_delay',         # 지연 최소화
        '-framedrop',                  # 프레임 드랍 허용 (끊김 방지)
        '-strict', 'experimental',     # 실험적 기능 허용
        'udp://0.0.0.0:5000'            # 모든 인터페이스로 수신
    ]

    print(f"[INFO] Listening for UDP stream on port 5000...")
    process = subprocess.Popen(command)

    return process
