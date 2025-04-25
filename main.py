from src.stream.ffmpeg_receiver import start_receiving

def main():
    process = start_receiving()

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping receiver...")
        process.terminate()

if __name__ == "__main__":
    main()
