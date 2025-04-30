# 📁 run_on_edge.py

import paramiko

# 💻 라즈베리파이 접속 정보
hostname = "192.168.0.20"   # 라즈베리파이 IP
port = 22
username = "drpill"
password = "drpill"  # 또는 ssh key 방식도 가능

# 📄 실행할 라즈베리 파일
remote_command = "nohup python3 /home/drpill/DrPill_edge/src/control/camera_controller.py > /dev/null 2>&1 &"



print(f"🔐 Connecting to {hostname}...")

# SSH 연결
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, port, username, password)

print(f"🚀 Running: {remote_command}")
stdin, stdout, stderr = ssh.exec_command(remote_command)
ssh.close()
print("✅ 명령 전송 완료 (백그라운드 실행)")

# # 실행 이후 출력 수집
# for line in stdout:
#     print("🚀", line, end="")

# for line in stderr:
#     print("❗", line, end="")

# # 👉 채널 및 세션 명확히 종료
# stdout.channel.shutdown_write()
# ssh.close()
