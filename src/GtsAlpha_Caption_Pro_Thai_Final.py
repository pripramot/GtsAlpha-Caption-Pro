# src/GtsAlpha_Caption_Pro_Thai_Final.py
# GtsAlpha Caption Pro - เวอร์ชันภาษาไทย

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
from gtts import gTTS
import datetime
import threading
import os

def log(message):
    log_text.configure(state='normal')
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {message}\n")
    log_text.see(tk.END)
    log_text.configure(state='disabled')

def extract_and_process():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("กรุณากรอกข้อมูล", "กรุณาวางลิงก์ YouTube")
        return

    def run():
        try:
            log("กำลังเริ่มทำงาน...")
            video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
            log(f"Video ID: {video_id}")

            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            en_text = " ".join([item['text'] for item in transcript])
            th_text = GoogleTranslator(source='en', target='th').translate(en_text)

            # สร้าง .srt
            def create_srt(transcript_list):
                srt = ""
                for i, item in enumerate(transcript_list):
                    start = str(datetime.timedelta(seconds=item['start'])) + ",000"
                    end = str(datetime.timedelta(seconds=item['start'] + item['duration'])) + ",000"
                    text = GoogleTranslator(source='en', target='th').translate(item['text'])
                    srt += f"{i+1}\n{start} --> {end}\n{text}\n\n"
                return srt

            with open(f"TH_{video_id}.srt", "w", encoding="utf-8") as f:
                f.write(create_srt(transcript))
            with open(f"EN_{video_id}.srt", "w", encoding="utf-8") as f:
                f.write(create_srt(transcript))

            # เสียงพากย์
            tts = gTTS(text=th_text, lang='th')
            tts.save(f"TH_{video_id}.mp3")

            log("เสร็จสิ้น! ไฟล์ .srt และ .mp3 ถูกสร้างแล้ว")
            messagebox.showinfo("สำเร็จ", "ประมวลผลเสร็จสมบูรณ์\nไฟล์ .srt และ .mp3 ถูกสร้างแล้ว")

        except Exception as e:
            log(f"เกิดข้อผิดพลาด: {str(e)}")
            messagebox.showerror("ผิดพลาด", str(e))

    threading.Thread(target=run, daemon=True).start()

# GUI
root = tk.Tk()
root.title("GtsAlpha Caption Pro")
root.geometry("800x600")
root.configure(bg="#0f172a")

tk.Label(root, text="GtsAlpha Caption Pro", font=("TH Sarabun New", 24, "bold"), bg="#0f172a", fg="#00d4ff").pack(pady=20)
tk.Label(root, text="ดึงคำบรรยาย YouTube แปลไทย + พากย์เสียง", font=("TH Sarabun New", 14), bg="#0f172a", fg="#e2e8f0").pack(pady=5)

tk.Label(root, text="วางลิงก์ YouTube:", font=("TH Sarabun New", 12), bg="#0f172a", fg="#e2e8f0").pack(pady=10)
url_entry = tk.Entry(root, font=("TH Sarabun New", 12), width=60, bg="#1e2937", fg="white")
url_entry.pack(pady=5)
url_entry.insert(0, "https://youtu.be/kJQP7kiw5Fk")

tk.Button(root, text="เริ่มประมวลผล", font=("TH Sarabun New", 14, "bold"), bg="#00d4ff", fg="#0f172a", command=extract_and_process).pack(pady=20)

log_text = scrolledtext.ScrolledText(root, height=12, bg="#1e2937", fg="#22c55e")
log_text.pack(pady=10, padx=20, fill="both", expand=True)

log("ระบบพร้อมใช้งาน - วางลิงก์แล้วกดปุ่มเริ่ม")

root.mainloop()
