# src/GtsAlpha_Caption_Pro_Thai_Final.py
# GtsAlpha Caption Pro - UI เวอร์ชันสวยงาม + ดาวน์โหลดวิดีโอ + เลือกโมเดล AI

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from deep_translator import GoogleTranslator
from gtts import gTTS
import datetime
import threading
import os
import requests

OLLAMA_API = "http://localhost:11434"

# ====================== Logging ======================

def log(msg):
    log_text.configure(state='normal')
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
    log_text.see(tk.END)
    log_text.configure(state='disabled')

# ====================== Video Download ======================

def download_video():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("กรุณากรอก URL", "วางลิงก์ YouTube หรือ X/Twitter ก่อนครับ")
        return

    def run():
        try:
            log(f"กำลังดาวน์โหลดวิดีโอจาก: {url}")
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'noplaylist': True,
                'quiet': False,
                'no_warnings': False,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            log("ดาวน์โหลดวิดีโอสำเร็จ ✓")
            messagebox.showinfo("สำเร็จ", "ดาวน์โหลดวิดีโอเสร็จสมบูรณ์\nไฟล์อยู่ในโฟลเดอร์เดียวกับโปรแกรม")
        except Exception as e:
            log(f"ดาวน์โหลดล้มเหลว: {str(e)}")
            messagebox.showerror("ผิดพลาด", f"ดาวน์โหลดไม่สำเร็จ\n{str(e)}\n\nโปรดตรวจสอบว่าเป็นวิดีโอสาธารณะ")

    threading.Thread(target=run, daemon=True).start()

# ====================== Caption + TTS ======================

def extract_caption_and_tts():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("กรุณากรอก URL", "วางลิงก์ก่อนครับ")
        return

    def run():
        try:
            log("กำลังดึงคำบรรยาย...")
            # แยก video_id จาก URL รูปแบบต่าง ๆ
            if "v=" in url:
                video_id = url.split("v=")[-1].split("&")[0]
            elif "youtu.be/" in url:
                video_id = url.split("youtu.be/")[-1].split("?")[0]
            else:
                video_id = url.rstrip("/").split("/")[-1].split("?")[0]
            log(f"Video ID: {video_id}")

            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            en_text = " ".join([item['text'] for item in transcript])
            th_text = GoogleTranslator(source='en', target='th').translate(en_text)

            def create_srt(items, translate=False):
                srt = ""
                for i, item in enumerate(items):
                    start = str(datetime.timedelta(seconds=int(item['start']))) + ",000"
                    end = str(datetime.timedelta(seconds=int(item['start'] + item['duration']))) + ",000"
                    text = GoogleTranslator(source='en', target='th').translate(item['text']) if translate else item['text']
                    srt += f"{i+1}\n{start} --> {end}\n{text}\n\n"
                return srt

            with open(f"TH_{video_id}.srt", "w", encoding="utf-8") as f:
                f.write(create_srt(transcript, translate=True))
            log("สร้าง TH_.srt สำเร็จ ✓")

            with open(f"EN_{video_id}.srt", "w", encoding="utf-8") as f:
                f.write(create_srt(transcript, translate=False))
            log("สร้าง EN_.srt สำเร็จ ✓")

            tts = gTTS(text=th_text, lang='th')
            tts.save(f"TH_{video_id}.mp3")
            log("สร้างเสียงพากย์ .mp3 สำเร็จ ✓")

            messagebox.showinfo("สำเร็จ", "สร้างไฟล์ .srt (EN/TH) และเสียงพากย์ (.mp3) เรียบร้อยแล้ว")
        except Exception as e:
            log(f"เกิดข้อผิดพลาด: {str(e)}")
            messagebox.showerror("ผิดพลาด", str(e))

    threading.Thread(target=run, daemon=True).start()

# ====================== Ollama Model Management ======================

# Default popular Ollama models shown before connecting
DEFAULT_MODELS = [
    "gemma2:9b",
    "gemma2:2b",
    "llama3:8b",
    "llama3:70b",
    "mistral:7b",
    "phi3:mini",
    "qwen2:7b",
]

def fetch_ollama_models():
    """Return list of locally installed Ollama model names, or DEFAULT_MODELS on error."""
    try:
        resp = requests.get(f"{OLLAMA_API}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            return models if models else DEFAULT_MODELS
    except Exception:
        pass
    return DEFAULT_MODELS

def refresh_models():
    """Refresh the model combobox with installed Ollama models."""
    log("กำลังตรวจสอบโมเดลที่ติดตั้งใน Ollama...")
    def run():
        models = fetch_ollama_models()
        root.after(0, lambda: _update_model_combo(models))
    threading.Thread(target=run, daemon=True).start()

def _update_model_combo(models):
    model_combo['values'] = models
    current = model_var.get()
    if current not in models:
        model_var.set(models[0] if models else "gemma2:9b")
    count = len(models)
    if models == DEFAULT_MODELS:
        log(f"Ollama ไม่ตอบสนอง — แสดงรายการโมเดลที่แนะนำ ({count} รายการ)")
    else:
        log(f"พบโมเดลที่ติดตั้งแล้ว {count} รายการ ✓")

# ====================== Gemma2 Summarize via Ollama ======================

def summarize_with_gemma():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("กรุณากรอก URL", "วางลิงก์ YouTube ก่อนครับ")
        return

    selected_model = model_var.get().strip()
    if not selected_model:
        messagebox.showwarning("กรุณาเลือกโมเดล", "เลือกโมเดล AI ก่อนกดสรุปครับ")
        return

    def run():
        try:
            log("กำลังดึงคำบรรยายเพื่อสรุป...")
            if "v=" in url:
                video_id = url.split("v=")[-1].split("&")[0]
            elif "youtu.be/" in url:
                video_id = url.split("youtu.be/")[-1].split("?")[0]
            else:
                video_id = url.rstrip("/").split("/")[-1].split("?")[0]

            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            en_text = " ".join([item['text'] for item in transcript])
            th_text = GoogleTranslator(source='en', target='th').translate(en_text)

            log(f"กำลังส่งข้อความให้ {selected_model} สรุป (ต้องรัน Ollama อยู่)...")
            payload = {
                "model": selected_model,
                "prompt": f"สรุปเนื้อหาต่อไปนี้เป็นภาษาไทยให้กระชับ:\n\n{th_text[:4000]}",
                "stream": False
            }
            response = requests.post(f"{OLLAMA_API}/api/generate", json=payload, timeout=120)
            if response.status_code == 200:
                summary = response.json().get("response", "")
                log(f"สรุปจาก {selected_model}:\n" + summary)
                messagebox.showinfo(f"สรุปจาก {selected_model}",
                                    summary[:500] + ("..." if len(summary) > 500 else ""))
            else:
                log(f"Ollama ตอบกลับ: {response.status_code}")
                messagebox.showerror("ผิดพลาด",
                                     f"ไม่สามารถเชื่อมต่อ Ollama ได้\nโปรดรัน: ollama run {selected_model}")
        except requests.exceptions.ConnectionError:
            log(f"ไม่พบ Ollama กรุณารัน: ollama run {selected_model}")
            messagebox.showerror("ไม่พบ Ollama",
                                 f"โปรดติดตั้งและรัน Ollama ก่อน\nคำสั่ง: ollama run {selected_model}")
        except Exception as e:
            log(f"เกิดข้อผิดพลาด: {str(e)}")
            messagebox.showerror("ผิดพลาด", str(e))

    threading.Thread(target=run, daemon=True).start()

# ====================== GUI ======================

root = tk.Tk()
root.title("GtsAlpha Caption Pro")
root.geometry("1000x820")
root.configure(bg="#0a0f1c")
root.resizable(True, True)

# สีหลัก
ACCENT = "#00d4ff"
BG = "#0a0f1c"
CARD = "#121a2e"
TEXT_LIGHT = "#e2e8f0"
TEXT_DIM = "#94a3b8"
TEXT_FOOTER = "#64748b"
LOG_FG = "#4ade80"

# Header
header = tk.Frame(root, bg=BG)
header.pack(fill="x", pady=(24, 4))
tk.Label(header, text="GtsAlpha", font=("TH Sarabun New", 44, "bold"), bg=BG, fg=ACCENT).pack()
tk.Label(header, text="Caption Pro", font=("TH Sarabun New", 18), bg=BG, fg=TEXT_DIM).pack(pady=2)

tk.Label(root, text="ดาวน์โหลดวิดีโอ • ดึงคำบรรยาย • แปลไทย • พากย์เสียง • สรุปด้วย AI",
         font=("TH Sarabun New", 13), bg=BG, fg="#cbd5e1").pack(pady=8)

# Input card
input_frame = tk.Frame(root, bg=CARD)
input_frame.pack(pady=20, padx=60, fill="x")

tk.Label(input_frame, text="วางลิงก์ YouTube หรือ X/Twitter (เฉพาะวิดีโอสาธารณะ)",
         font=("TH Sarabun New", 13), bg=CARD, fg=TEXT_LIGHT).pack(pady=(16, 6))

url_entry = tk.Entry(input_frame, font=("TH Sarabun New", 14), width=70,
                     bg="#1e2937", fg="#f1f5f9", relief="flat",
                     insertbackground=ACCENT,
                     highlightthickness=2, highlightcolor=ACCENT)
url_entry.pack(pady=8, padx=40, ipady=8)
url_entry.insert(0, "https://youtu.be/kJQP7kiw5Fk")
tk.Frame(input_frame, bg=CARD, height=10).pack()

# ── Model selector row ──────────────────────────────────────────────────────
model_frame = tk.Frame(root, bg=BG)
model_frame.pack(pady=(4, 0))

tk.Label(model_frame, text="🤖  โมเดล AI:", font=("TH Sarabun New", 13, "bold"),
         bg=BG, fg=TEXT_LIGHT).grid(row=0, column=0, padx=(0, 8))

model_var = tk.StringVar(value=DEFAULT_MODELS[0])
model_combo = ttk.Combobox(model_frame, textvariable=model_var,
                            values=DEFAULT_MODELS, width=28,
                            font=("TH Sarabun New", 13), state="normal")
model_combo.grid(row=0, column=1, padx=6)

tk.Button(model_frame, text="🔄",
          font=("TH Sarabun New", 12), relief="flat", cursor="hand2",
          bg="#1e3a5f", fg=ACCENT, activebackground="#1e2937",
          padx=8, pady=4,
          command=refresh_models).grid(row=0, column=2, padx=6)

tk.Label(model_frame, text="← รีเฟรชโมเดลจาก Ollama",
         font=("TH Sarabun New", 11), bg=BG, fg=TEXT_DIM).grid(row=0, column=3, padx=4)
# ────────────────────────────────────────────────────────────────────────────

# Buttons
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=18)

btn_cfg = dict(font=("TH Sarabun New", 13, "bold"), relief="flat", cursor="hand2",
               activeforeground="#0a0f1c", padx=18, pady=10)

tk.Button(btn_frame, text="📥  ดาวน์โหลดวิดีโอ",
          bg=ACCENT, fg="#0a0f1c", activebackground="#38bdf8",
          command=download_video, **btn_cfg).grid(row=0, column=0, padx=10, pady=6)

tk.Button(btn_frame, text="📝  ดึง Caption + แปล + พากย์",
          bg="#22c55e", fg="#0a0f1c", activebackground="#4ade80",
          command=extract_caption_and_tts, **btn_cfg).grid(row=0, column=1, padx=10, pady=6)

tk.Button(btn_frame, text="🤖  สรุปด้วย AI",
          bg="#a855f7", fg="#ffffff", activebackground="#c084fc",
          command=summarize_with_gemma, **btn_cfg).grid(row=0, column=2, padx=10, pady=6)

# Log area
log_frame = tk.LabelFrame(root, text="  สถานะการทำงาน  ",
                           font=("TH Sarabun New", 12, "bold"),
                           bg=CARD, fg=ACCENT, padx=12, pady=8)
log_frame.pack(pady=16, padx=50, fill="both", expand=True)

log_text = scrolledtext.ScrolledText(log_frame, height=14,
                                     font=("Consolas", 11),
                                     bg="#0f172a", fg=LOG_FG, relief="flat",
                                     state='disabled')
log_text.pack(padx=8, pady=8, fill="both", expand=True)

# Footer
tk.Label(root,
         text="GtsAlpha Caption Pro  •  รองรับ YouTube & X/Twitter (สาธารณะ)  •  AI ผ่าน Ollama",
         font=("TH Sarabun New", 10), bg=BG, fg=TEXT_FOOTER).pack(side="bottom", pady=12)

log("ระบบพร้อมใช้งาน • วางลิงก์ YouTube หรือ X/Twitter แล้วกดปุ่ม")
log("กด 🔄 เพื่อโหลดรายการโมเดลที่ติดตั้งใน Ollama")

root.mainloop()
