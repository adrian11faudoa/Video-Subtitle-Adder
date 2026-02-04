import whisper
import subprocess
from deep_translator import GoogleTranslator
import pysrt
import os

VIDEO_FILE = "input_video.mp4"
AUDIO_FILE = "audio.wav"
SRT_FILE = "subtitles_en.srt"

# -------------------------
# STEP 1: Extract Audio
# -------------------------
def extract_audio():
    print("Extracting audio...")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", VIDEO_FILE,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        AUDIO_FILE
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Audio extracted.")

# -------------------------
# STEP 2: Speech to Text (Japanese)
# -------------------------
def transcribe_audio():
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing Japanese audio...")
    result = model.transcribe(AUDIO_FILE, language="ja")

    return result["segments"]

# -------------------------
# STEP 3: Translate JP → EN
# -------------------------
def translate_text(text):
    try:
        return GoogleTranslator(source='ja', target='en').translate(text)
    except:
        return text

# -------------------------
# STEP 4: Create SRT File
# -------------------------
def create_srt(segments):
    print("Creating SRT file...")
    subs = pysrt.SubRipFile()

    for i, seg in enumerate(segments, start=1):
        start = seg["start"]
        end = seg["end"]
        jp_text = seg["text"].strip()
        en_text = translate_text(jp_text)

        sub = pysrt.SubRipItem(
            index=i,
            start=pysrt.SubRipTime(seconds=start),
            end=pysrt.SubRipTime(seconds=end),
            text=en_text
        )

        subs.append(sub)

    subs.save(SRT_FILE, encoding='utf-8')
    print("SRT created:", SRT_FILE)

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    extract_audio()
    segments = transcribe_audio()
    create_srt(segments)

    print("\nDone!")
