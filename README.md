# GtsAlpha Caption Pro

เครื่องมือ Python สำหรับดึงคำบรรยาย YouTube แปลไทย + พากย์เสียงไทย + สรุปด้วย AI

### ฟีเจอร์หลัก
- ดาวน์โหลดวิดีโอจาก YouTube และ X/Twitter (เฉพาะสาธารณะ) ด้วย yt-dlp
- ดึงคำบรรยายจากวิดีโอ YouTube
- แปลเป็นภาษาไทยอัตโนมัติ
- บันทึกเป็นไฟล์ .srt (EN และ TH พร้อม timestamp)
- สร้างเสียงพากย์ไทย (.mp3)
- **เลือกโมเดล AI ได้จาก GUI** — รีเฟรชรายการโมเดลที่ติดตั้งใน Ollama แบบ real-time
- รองรับโมเดลทุกตัวที่ run บน Ollama เช่น Gemma2 9B, Llama3, Mistral, Phi3 ฯลฯ
- GUI ภาษาไทย Dark Theme
- **เลือกโฟลเดอร์บันทึกไฟล์** ได้จาก GUI
- **URL validation** — ตรวจสอบลิงก์อัตโนมัติก่อนประมวลผล
- **Retry logic** — ระบบลองใหม่อัตโนมัติเมื่อเครือข่ายมีปัญหา

---

### โครงสร้างโปรเจกต์

```
src/
  gtsalpha/
    __init__.py          # Package metadata
    __main__.py          # Entry point (python -m gtsalpha)
    core/
      caption.py         # Transcript extraction + SRT generation
      downloader.py      # yt-dlp video downloader
      summarizer.py      # Ollama AI summarization client
      translator.py      # Google Translate wrapper with retries
      tts.py             # Text-to-speech (gTTS)
    gui/
      app.py             # Main Tk application window
      theme.py           # Colors, fonts, style constants
      widgets.py         # Thread-safe log panel widget
    utils/
      config.py          # Application constants
      url_parser.py      # YouTube URL parsing & validation
  GtsAlpha_Caption_Pro_Thai_Final.py  # Backward-compatible entry point
tests/                   # Unit tests (pytest)
```

---

### วิธีรันแบบ Python (สำหรับ Developer)

```bash
pip install -r requirements.txt
python src/GtsAlpha_Caption_Pro_Thai_Final.py

# หรือรันเป็น module:
PYTHONPATH=src python -m gtsalpha
```

---

### วิธีรันเทสต์

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest tests/ -v
```

---

### วิธีสร้างไฟล์ติดตั้ง (.exe) สำหรับ Windows

#### ขั้นตอน
1. ติดตั้ง [Python 3.9+](https://www.python.org/downloads/) (ติ๊ก "Add Python to PATH")
2. ดับเบิลคลิกที่ไฟล์ **`build_installer.bat`** ในโฟลเดอร์โปรเจกต์
3. รอ build เสร็จ → ไฟล์ `.exe` จะอยู่ที่ `dist\GtsAlpha_Caption_Pro.exe`
4. คัดลอก `dist\GtsAlpha_Caption_Pro.exe` ไปวางที่ไหนก็ได้ แล้วดับเบิลคลิกรัน

#### Linux / macOS
```bash
chmod +x build_installer.sh
./build_installer.sh
# ไฟล์อยู่ที่ dist/GtsAlpha_Caption_Pro
```

---

### ใช้งานฟีเจอร์สรุปด้วย AI (Ollama)

1. ติดตั้ง [Ollama](https://ollama.com)
2. ดาวน์โหลดโมเดลที่ต้องการ เช่น:
   ```bash
   ollama run gemma2:9b
   # หรือ
   ollama run llama3:8b
   # หรือ
   ollama run mistral:7b
   ```
3. เปิดโปรแกรม → กด **🔄** เพื่อโหลดรายการโมเดลที่ติดตั้งแล้ว → เลือกโมเดล → กด **🤖 สรุปด้วย AI**

### ความต้องการของระบบ (สำหรับ Gemma2 9B)
| รายการ | ขั้นต่ำ | แนะนำ |
|---|---|---|
| RAM | 12 GB | 16 GB+ |
| GPU VRAM | 6 GB (4-bit) | 8 GB+ |
| พื้นที่ดิสก์ | 6 GB (โมเดล) | 20 GB+ |

พัฒนาเพื่อใช้ในงานวิจัยเรื่องระบบอัตโนมัติและการตลาดโซเชียลมีเดีย
