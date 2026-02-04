import tkinter as tk
from tkinter import filedialog, messagebox
import whisper
import threading
import os

# =====================
# LOAD MODEL
# =====================
model = whisper.load_model("base")


# =====================
# TIME FORMAT FUNCTION
# =====================
def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


# =====================
# TRANSCRIPTION FUNCTION
# =====================
def transcribe_file(file_path):
    try:
        result = model.transcribe(
            file_path,
            task="translate"
        )

        srt_path = os.path.splitext(file_path)[0] + ".srt"

        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start = format_time(segment["start"])
                end = format_time(segment["end"])
                text = segment["text"].strip()

                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

        messagebox.showinfo("Done", f"Saved:\n{srt_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# =====================
# FILE SELECTOR
# =====================
def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Media files", "*.mp3 *.wav *.m4a *.mp4 *.mkv *.mov"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        status_label.config(text="Processing...")
        threading.Thread(
            target=run_transcription,
            args=(file_path,),
            daemon=True
        ).start()


def run_transcription(file_path):
    transcribe_file(file_path)
    status_label.config(text="Ready")


# =====================
# UI
# =====================
root = tk.Tk()
root.title("JP → EN Subtitle Generator")
root.geometry("420x220")

title = tk.Label(
    root,
    text="Japanese → English Subtitle Generator",
    font=("Arial", 14)
)
title.pack(pady=20)

btn = tk.Button(
    root,
    text="Select Audio / Video",
    command=select_file,
    height=2,
    width=25
)
btn.pack(pady=10)

status_label = tk.Label(root, text="Ready")
status_label.pack(pady=15)

root.mainloop()
