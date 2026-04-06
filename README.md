# GtsAlpha Caption Pro

เครื่องมือ Python สำหรับดึงคำบรรยาย YouTube แปลไทย + พากย์เสียงไทย

### ฟีเจอร์หลัก
- ดาวน์โหลดวิดีโอจาก YouTube และ X/Twitter (เฉพาะสาธารณะ) ด้วย yt-dlp
- ดึงคำบรรยายจากวิดีโอ YouTube
- แปลเป็นภาษาไทยอัตโนมัติ
- บันทึกเป็นไฟล์ .srt (EN และ TH พร้อม timestamp)
- สร้างเสียงพากย์ไทย (.mp3)
- สรุปเนื้อหาด้วย Gemma2 9B ผ่าน Ollama
- GUI ภาษาไทย Dark Theme

### วิธีใช้งาน

1. ติดตั้งไลบรารี
   ```bash
   pip install -r requirements.txt
   ```

2. รันโปรแกรม
   ```bash
   python src/GtsAlpha_Caption_Pro_Thai_Final.py
   ```

3. (ถ้าต้องการใช้ปุ่มสรุป Gemma2 9B) ติดตั้ง [Ollama](https://ollama.com) แล้วรัน
   ```bash
   ollama run gemma2:9b
   ```

### ความต้องการของระบบ (สำหรับ Gemma2 9B)
- RAM อย่างน้อย 12 GB (แนะนำ 16 GB+)
- GPU VRAM 6 GB+ สำหรับ 4-bit quantized (~5.4 GB)
- พื้นที่ดิสก์ว่างประมาณ 6 GB

พัฒนาเพื่อใช้ในงานวิจัยเรื่องระบบอัตโนมัติและการตลาดโซเชียลมีเดีย
