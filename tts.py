import openai
import os
from datetime import datetime
from pydub import AudioSegment
import re

# 🔑 OpenAI API 키
openai.api_key = "sk-..."  # 본인의 키로 바꾸세요

def generate_and_play_tts(text: str, voice: str = "fable"):
    if not text.strip():
        print("⚠️ 입력된 텍스트가 비어 있습니다.")
        return

    print(f"📖 읽을 텍스트: {text}")

    # 파일명에 쓸 수 있는 형태로 정리 (공백 → _, 특수문자 제거, 최대 30자)
    safe_title = re.sub(r"[^\w\s]", "", text)
    safe_title = "_".join(safe_title.strip().split())[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("tts_output", exist_ok=True)
    mp3_path = f"tts_output/{safe_title}_{timestamp}.mp3"
    wav_path = f"tts_output/{safe_title}_{timestamp}.wav"

    try:
        print("🛠️ OpenAI TTS 생성 중...")
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        with open(mp3_path, "wb") as f:
            f.write(response.content)
        print(f"✅ MP3 저장 완료: {mp3_path}")

        print("🔄 MP3 → WAV 변환 중...")
        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")
        print(f"✅ WAV 저장 완료: {wav_path}")

        print("🔊 재생 시작...")
        os.system(f"aplay -D plughw:2,0 {wav_path}")

    except Exception as e:
        print("❌ 오류 발생:", e)

