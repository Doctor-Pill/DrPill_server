# 📍 DRPILL_SERVER/src/config/settings.py

# 🔗 네트워크 설정
HOST = '0.0.0.0'
PORT = 5000
SECRET_KEY = 'secret!'

# 🖥️ 워크스테이션 브라우저 설정
ADMIN_BROWSER_URL = f'http://localhost:{PORT}/admin'
ADMIN_BROWSER_CMD = [
    'google-chrome',
    '--new-window',
    '--noerrdialogs',
    ADMIN_BROWSER_URL
]

# 🍓 라즈베리파이 브라우저 설정
RASPBERRY_PI_IP = '192.168.0.20'
RASPBERRY_CLIENT_URL = f'http://192.168.0.10:{PORT}/client'
RASPBERRY_BROWSER_CMD = (
    f'DISPLAY=:0 chromium-browser --noerrdialogs '
    f'--use-fake-ui-for-media-stream --kiosk {RASPBERRY_CLIENT_URL}'
)
RASPBERRY_CLOSE_CMD = "pkill -9 -f 'chromium.*kiosk'"

# 🎥 ffplay 수신 설정
UDP_STREAM_PORT = 5000
FFPLAY_CMD = [
    'ffplay',
    '-fflags', 'nobuffer',
    '-flags', 'low_delay',
    '-framedrop',
    '-strict', 'experimental',
    f'udp://0.0.0.0:{UDP_STREAM_PORT}'
]
