# GtsAlpha Caption Pro

<div align="center">

🎬 **Desktop App ดึงคำบรรยาย YouTube · แปลไทย · พากย์เสียง · AI สรุป**

[![Tauri v2](https://img.shields.io/badge/Tauri-v2-24C8D8?logo=tauri)](https://tauri.app)
[![Rust](https://img.shields.io/badge/Rust-1.77+-orange?logo=rust)](https://www.rust-lang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](https://github.com/pripramot/GtsAlpha-Caption-Pro/releases)

</div>

---

## ภาพรวมโครงการ

**GtsAlpha Caption Pro** คือ Desktop Application ที่สร้างด้วย **Tauri v2** (Rust + WebView)
ออกแบบมาเพื่อ:

- 📥 **ดึงคำบรรยาย** (Subtitle / Caption) จาก YouTube และ X/Twitter
- 🌏 **แปลเป็นภาษาไทย** อัตโนมัติ พร้อมบันทึกเป็นไฟล์ `.srt`
- 🔊 **สร้างเสียงพากย์ไทย** (.mp3) ด้วย gTTS
- 🤖 **สรุปเนื้อหาด้วย AI** ผ่าน Ollama (ทำงาน Offline บนเครื่อง)
- 📹 **ดาวน์โหลดวิดีโอ** ด้วย yt-dlp

---

## สถาปัตยกรรม

```
GtsAlpha Caption Pro
├── Frontend  — HTML / CSS / Vanilla JavaScript
│               Dark Theme · ภาษาไทย · Responsive
├── Backend   — Rust (Tauri v2 Commands)
│               ประมวลผลหลัก · API calls · File I/O
└── WebView   — ระบบปฏิบัติการ (ไม่ฝัง Chromium)
                WebView2 (Windows) · WKWebView (macOS) · WebKitGTK (Linux)
```

### ทำไม Tauri v2? (ไม่ใช่ Electron)

| รายการ | Tauri v2 | Electron |
|---|---|---|
| Chromium | ❌ ไม่ฝัง | ✅ ฝังอยู่ใน package |
| ขนาดโปรแกรม | ~3–10 MB | ~120–200 MB |
| RAM ขณะรัน | น้อยกว่า | สูงกว่า (รัน Chromium แยก) |
| Backend | Rust | Node.js |
| ความปลอดภัย | Rust memory safety | ขึ้นอยู่กับ JS |

> Tauri ใช้ WebView ที่มีอยู่แล้วในระบบปฏิบัติการ จึงเบาและเร็วกว่า Electron มาก

---

## ความต้องการของระบบ

### สำหรับ Developer (Build จาก Source)

| รายการ | เวอร์ชัน |
|---|---|
| [Rust](https://rustup.rs) | 1.77.2+ |
| [Node.js](https://nodejs.org) | 18.0.0+ |
| npm | 9.0.0+ |
| WebView2 Runtime (Windows) | ติดตั้งอัตโนมัติ |

**Linux** ต้องการ library เพิ่มเติม:

```bash
# Ubuntu / Debian
sudo apt install libwebkit2gtk-4.1-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev

# Fedora
sudo dnf install webkit2gtk4.1-devel gtk3-devel
```

### สำหรับฟีเจอร์ AI Summarize (Ollama)

| รายการ | ขั้นต่ำ | แนะนำ |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| GPU VRAM (4-bit) | 6 GB | 8 GB+ |
| พื้นที่ดิสก์ (โมเดล) | 5 GB | 20 GB+ |

---

## ขั้นตอนการติดตั้ง

### 1. Clone Repository

```bash
git clone https://github.com/pripramot/GtsAlpha-Caption-Pro.git
cd GtsAlpha-Caption-Pro
```

### 2. ติดตั้ง Rust

```bash
# macOS / Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Windows: ดาวน์โหลด rustup-init.exe จาก https://rustup.rs
```

### 3. ติดตั้ง Node.js Dependencies

```bash
npm install
```

### 4. ติดตั้ง Tauri CLI (Optional)

```bash
npm install -g @tauri-apps/cli@^2
# หรือใช้ผ่าน npx โดยตรง
```

---

## วิธี Build และ Run

### Development Mode (Hot Reload)

```bash
npm run dev
# หรือ
npx tauri dev
```

### Production Build

```bash
npm run build
# หรือ
npx tauri build
```

ไฟล์ติดตั้งจะอยู่ที่:

| OS | ที่อยู่ไฟล์ |
|---|---|
| Windows | `src-tauri/target/release/bundle/msi/*.msi` |
| macOS | `src-tauri/target/release/bundle/dmg/*.dmg` |
| Linux | `src-tauri/target/release/bundle/appimage/*.AppImage` |

---

## ขั้นตอนการ Publish Package

### npm Publish

```bash
# 1. เข้าสู่ระบบ npmjs.com
npm login

# 2. ตรวจสอบ package.json และ version
cat package.json

# 3. Publish
npm publish --access public

# 4. ยืนยันผล
npm view gtsalpha-caption-pro
```

### GitHub Release (Desktop App Binary)

```bash
# 1. Build
npm run build

# 2. สร้าง Git Tag
git tag v1.0.0
git push origin v1.0.0

# 3. สร้าง Release บน GitHub → อัปโหลด binary
# https://github.com/pripramot/GtsAlpha-Caption-Pro/releases/new
```

---

## โครงสร้างโปรเจกต์

```
GtsAlpha-Caption-Pro/
├── src/                          # Frontend (HTML / CSS / JS)
│   ├── index.html                # หน้า UI หลักของ App
│   ├── styles.css                # Dark Theme Styles
│   └── main.js                  # Logic + Tauri API calls
├── src-tauri/                    # Backend (Rust)
│   ├── Cargo.toml                # Rust dependencies
│   ├── tauri.conf.json           # Tauri configuration
│   ├── build.rs                  # Build script
│   ├── capabilities/
│   │   └── default.json          # Tauri v2 permissions
│   ├── icons/                    # App icons
│   └── src/
│       ├── main.rs               # Entry point
│       └── lib.rs                # Tauri commands (Rust)
├── src/gtsalpha/                 # Python package (core logic)
│   ├── core/                     # Caption, Translate, TTS, AI
│   ├── gui/                      # Tkinter GUI (legacy)
│   └── utils/                    # Utilities
├── index.html                    # หน้าประชาสัมพันธ์โครงการ
├── package.json                  # npm package config
├── pyproject.toml                # Python package config
├── TASK.md                       # Task Checklist
└── README.md                     # เอกสารนี้
```

---

## วิธีใช้งาน (คู่มือภาษาไทย)

### 1. ดึงคำบรรยาย

1. เปิดโปรแกรมด้วย `npm run dev`
2. ไปแท็บ **📥 ดึงคำบรรยาย**
3. วาง URL YouTube ในช่อง **ลิงก์วิดีโอ**
4. เลือกภาษาคำบรรยายต้นทาง
5. กด 📁 เลือกโฟลเดอร์บันทึกไฟล์
6. เลือก checkbox ที่ต้องการ (แปลไทย / TTS / ดาวน์โหลด)
7. กด **▶️ เริ่มประมวลผล**

### 2. แปลคำบรรยาย

1. ไปแท็บ **🌏 แปลภาษา**
2. กด **📁 เลือกไฟล์** เลือกไฟล์ `.srt` ที่มีอยู่
3. เลือกภาษาต้นทาง
4. กด **🌏 แปลเป็นภาษาไทย**

### 3. สร้างเสียงพากย์ (TTS)

1. ไปแท็บ **🔊 พากย์เสียงไทย**
2. เลือกไฟล์ `.srt` ภาษาไทย
3. เลือกความเร็วเสียง
4. กด **🔊 สร้างเสียงพากย์**

### 4. AI สรุปเนื้อหา (Ollama)

1. ติดตั้ง [Ollama](https://ollama.com)
2. ดาวน์โหลดโมเดล:
   ```bash
   ollama pull gemma2:9b
   # หรือ
   ollama pull llama3:8b
   ```
3. ไปแท็บ **🤖 สรุปด้วย AI**
4. กด **🔄** เพื่อโหลดรายการโมเดล
5. วางข้อความและกด **🤖 สรุปด้วย AI**

---

## Tests (Python)

```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest tests/ -v
```

---

## Contributing

1. Fork repository
2. สร้าง branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "feat: add your feature"`
4. Push: `git push origin feature/your-feature`
5. เปิด Pull Request

---

## License

MIT © 2025 [GtsAlpha](https://github.com/pripramot)
