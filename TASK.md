# GtsAlpha Caption Pro — Task Checklist

รายการงานทั้งหมดสำหรับการพัฒนาและเผยแพร่ **GtsAlpha Caption Pro** บน Tauri v2

---

## ✅ Phase 1: ตั้งค่าโครงสร้างโปรเจกต์ Tauri v2

- [x] สร้างไฟล์ `src-tauri/Cargo.toml` — กำหนด Rust dependencies (tauri v2, serde, reqwest, tokio)
- [x] สร้างไฟล์ `src-tauri/build.rs` — Tauri build script
- [x] สร้างไฟล์ `src-tauri/src/main.rs` — Entry point
- [x] สร้างไฟล์ `src-tauri/src/lib.rs` — Tauri commands (validate_url, extract_video_id, check_ollama_status, list_ollama_models)
- [x] สร้างไฟล์ `src-tauri/tauri.conf.json` — App config, window, bundle settings
- [x] สร้างไฟล์ `src-tauri/capabilities/default.json` — Tauri v2 permissions
- [ ] เพิ่ม App Icons ที่ `src-tauri/icons/` (32x32, 128x128, icon.ico, icon.icns)
- [ ] รัน `npx tauri icon <image>` เพื่อสร้าง icons อัตโนมัติ

---

## ✅ Phase 2: พัฒนา Frontend

- [x] สร้างไฟล์ `src/index.html` — UI หลัก (5 แท็บ: ดึงคำบรรยาย, แปล, TTS, AI, ตั้งค่า)
- [x] สร้างไฟล์ `src/styles.css` — Dark Theme UI ภาษาไทย
- [x] สร้างไฟล์ `src/main.js` — Logic + Tauri API integration
- [ ] ทดสอบ UI ใน browser ก่อน (เปิด `src/index.html` ตรงๆ)
- [ ] ทดสอบ Tauri commands ผ่าน `npm run dev`

---

## ✅ Phase 3: สร้าง Backend Commands (Rust)

- [x] `get_app_version` — ดึงเวอร์ชันจาก Cargo.toml
- [x] `get_default_config` — คืนค่า default configuration
- [x] `validate_url` — ตรวจสอบ URL (YouTube/X/Twitter)
- [x] `extract_video_id` — ดึง Video ID จาก YouTube URL
- [x] `check_ollama_status` — ตรวจสอบว่า Ollama service รันอยู่
- [x] `list_ollama_models` — ดึงรายการโมเดลจาก Ollama API
- [ ] เพิ่ม command สำหรับเรียก Python script ผ่าน shell (yt-dlp, gTTS)
- [ ] เพิ่ม command สำหรับ file operations (save SRT, save MP3)
- [ ] เพิ่ม error handling ครบทุก command

---

## ✅ Phase 4: npm Package & Publish

- [x] สร้างไฟล์ `package.json` — กำหนด name, version, scripts, dependencies
- [ ] รัน `npm install` เพื่อติดตั้ง `@tauri-apps/api` และ `@tauri-apps/cli`
- [ ] สมัครบัญชี [npmjs.com](https://www.npmjs.com) (หากยังไม่มี)
- [ ] รัน `npm login` เพื่อเข้าสู่ระบบ
- [ ] รัน `npm publish --access public` เพื่อเผยแพร่ package
- [ ] ยืนยันผลที่ `https://www.npmjs.com/package/gtsalpha-caption-pro`

---

## ✅ Phase 5: Build & Release

- [ ] รัน `npm run build` บน Windows เพื่อสร้าง `.msi` / `.exe`
- [ ] รัน `npm run build` บน macOS เพื่อสร้าง `.dmg`
- [ ] รัน `npm run build` บน Linux เพื่อสร้าง `.AppImage` / `.deb`
- [ ] ทดสอบการติดตั้งบนแต่ละ OS
- [ ] สร้าง Git Tag `v1.0.0`: `git tag v1.0.0 && git push origin v1.0.0`
- [ ] สร้าง GitHub Release พร้อมอัปโหลด binary ทุก platform
- [ ] อัปเดตลิงก์ดาวน์โหลดใน `index.html`

---

## ✅ Phase 6: เอกสาร & ประชาสัมพันธ์

- [x] เขียน `README.md` ใหม่ทั้งหมด (ภาพรวม, สถาปัตยกรรม, ติดตั้ง, build, publish)
- [x] สร้าง `index.html` หน้าเดียวสำหรับประชาสัมพันธ์โครงการ (พร้อม placeholder ลิงก์)
- [x] สร้าง `TASK.md` checklist งานทั้งหมด (ไฟล์นี้)
- [ ] อัปเดต placeholder ลิงก์ใน `index.html` เมื่อมี Release จริง
- [ ] เพิ่ม screenshot / demo GIF ใน README.md
- [ ] Deploy `index.html` ไปยัง GitHub Pages:
  - ไปที่ Settings → Pages → Source: Deploy from branch → เลือก `main` / `/ (root)`

---

## ✅ Phase 7: CI/CD (GitHub Actions)

- [ ] สร้าง `.github/workflows/release.yml` สำหรับ auto-build multi-platform เมื่อ push tag
- [ ] ตั้งค่า matrix build: windows-latest, macos-latest, ubuntu-latest
- [ ] ตั้งค่า cache สำหรับ Rust และ Node.js
- [ ] ทดสอบ workflow

---

## ✅ Phase 8: ทดสอบและ QA

- [ ] ทดสอบดึงคำบรรยายจาก YouTube URL จริง
- [ ] ทดสอบแปลภาษาไทย
- [ ] ทดสอบ TTS
- [ ] ทดสอบ AI summarize ด้วย Ollama (gemma2, llama3)
- [ ] ทดสอบ URL validation (ถูก/ผิด)
- [ ] ทดสอบบน Windows, macOS, Linux
- [ ] ทดสอบ error handling (ไม่มีอินเทอร์เน็ต, Ollama ปิด ฯลฯ)

---

## สรุปความคืบหน้า

| Phase | สถานะ |
|---|---|
| 1. โครงสร้าง Tauri v2 | ✅ เสร็จแล้ว (รอ icons) |
| 2. Frontend UI | ✅ เสร็จแล้ว |
| 3. Rust Backend Commands | ✅ เสร็จแล้ว (core commands) |
| 4. npm Publish | 🔲 รอดำเนินการ |
| 5. Build & Release | 🔲 รอดำเนินการ |
| 6. เอกสาร | ✅ เสร็จแล้ว |
| 7. CI/CD | 🔲 รอดำเนินการ |
| 8. QA | 🔲 รอดำเนินการ |
