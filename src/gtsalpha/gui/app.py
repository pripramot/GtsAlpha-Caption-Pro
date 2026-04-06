"""Main application window for GtsAlpha Caption Pro."""

from __future__ import annotations

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from gtsalpha.core import caption, summarizer, tts
from gtsalpha.core.downloader import download_video
from gtsalpha.core.translator import translate_text
from gtsalpha.gui import theme as T
from gtsalpha.gui.widgets import LogPanel
from gtsalpha.utils.config import DEFAULT_MODELS
from gtsalpha.utils.url_parser import InvalidURLError, extract_video_id, validate_url


class App:
    """GtsAlpha Caption Pro main application."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("GtsAlpha Caption Pro")
        self.root.geometry("1000x820")
        self.root.configure(bg=T.BG)
        self.root.resizable(True, True)

        self.output_dir = os.getcwd()

        self._build_header()
        self._build_input_card()
        self._build_model_selector()
        self._build_buttons()
        self._build_log_area()
        self._build_footer()

        self.log("ระบบพร้อมใช้งาน • วางลิงก์ YouTube หรือ X/Twitter แล้วกดปุ่ม")
        self.log("กด 🔄 เพื่อโหลดรายการโมเดลที่ติดตั้งใน Ollama")

    # ── Layout builders ─────────────────────────────────────────────────────

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=T.BG)
        header.pack(fill="x", pady=(24, 4))
        tk.Label(header, text="GtsAlpha", font=T.FONT_TITLE, bg=T.BG, fg=T.ACCENT).pack()
        tk.Label(header, text="Caption Pro", font=T.FONT_SUBTITLE, bg=T.BG, fg=T.TEXT_DIM).pack(
            pady=2
        )
        tk.Label(
            self.root,
            text="ดาวน์โหลดวิดีโอ • ดึงคำบรรยาย • แปลไทย • พากย์เสียง • สรุปด้วย AI",
            font=T.FONT_BODY,
            bg=T.BG,
            fg=T.TEXT_SUBTITLE,
        ).pack(pady=8)

    def _build_input_card(self) -> None:
        input_frame = tk.Frame(self.root, bg=T.CARD)
        input_frame.pack(pady=20, padx=60, fill="x")

        tk.Label(
            input_frame,
            text="วางลิงก์ YouTube หรือ X/Twitter (เฉพาะวิดีโอสาธารณะ)",
            font=T.FONT_BODY,
            bg=T.CARD,
            fg=T.TEXT_LIGHT,
        ).pack(pady=(16, 6))

        self.url_entry = tk.Entry(
            input_frame,
            font=T.FONT_ENTRY,
            width=70,
            bg=T.ENTRY_BG,
            fg=T.ENTRY_FG,
            relief="flat",
            insertbackground=T.ACCENT,
            highlightthickness=2,
            highlightcolor=T.ACCENT,
        )
        self.url_entry.pack(pady=8, padx=40, ipady=8)
        self.url_entry.insert(0, "https://youtu.be/kJQP7kiw5Fk")

        # Output directory row
        dir_frame = tk.Frame(input_frame, bg=T.CARD)
        dir_frame.pack(pady=(4, 12), padx=40, fill="x")
        tk.Label(
            dir_frame, text="📁 บันทึกไฟล์ที่:", font=T.FONT_SMALL, bg=T.CARD, fg=T.TEXT_DIM
        ).pack(side="left")
        self._dir_label = tk.Label(
            dir_frame,
            text=self.output_dir,
            font=T.FONT_SMALL,
            bg=T.CARD,
            fg=T.TEXT_LIGHT,
            anchor="w",
        )
        self._dir_label.pack(side="left", padx=6, fill="x", expand=True)
        tk.Button(
            dir_frame,
            text="เลือกโฟลเดอร์",
            font=T.FONT_SMALL,
            relief="flat",
            bg=T.BTN_REFRESH_BG,
            fg=T.ACCENT,
            cursor="hand2",
            command=self._pick_output_dir,
        ).pack(side="right")

    def _build_model_selector(self) -> None:
        model_frame = tk.Frame(self.root, bg=T.BG)
        model_frame.pack(pady=(4, 0))

        tk.Label(
            model_frame,
            text="🤖  โมเดล AI:",
            font=T.FONT_BODY_BOLD,
            bg=T.BG,
            fg=T.TEXT_LIGHT,
        ).grid(row=0, column=0, padx=(0, 8))

        self.model_var = tk.StringVar(value=DEFAULT_MODELS[0])
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=DEFAULT_MODELS,
            width=28,
            font=T.FONT_BODY,
            state="normal",
        )
        self.model_combo.grid(row=0, column=1, padx=6)

        tk.Button(
            model_frame,
            text="🔄",
            font=T.FONT_REFRESH,
            relief="flat",
            cursor="hand2",
            bg=T.BTN_REFRESH_BG,
            fg=T.ACCENT,
            activebackground=T.ENTRY_BG,
            padx=8,
            pady=4,
            command=self._refresh_models,
        ).grid(row=0, column=2, padx=6)

        tk.Label(
            model_frame,
            text="← รีเฟรชโมเดลจาก Ollama",
            font=T.FONT_SMALL,
            bg=T.BG,
            fg=T.TEXT_DIM,
        ).grid(row=0, column=3, padx=4)

    def _build_buttons(self) -> None:
        btn_frame = tk.Frame(self.root, bg=T.BG)
        btn_frame.pack(pady=18)

        btn_cfg: dict = dict(
            font=T.FONT_BTN,
            relief="flat",
            cursor="hand2",
            activeforeground=T.BG,
            padx=18,
            pady=10,
        )

        tk.Button(
            btn_frame,
            text="📥  ดาวน์โหลดวิดีโอ",
            bg=T.BTN_DOWNLOAD_BG,
            fg=T.BTN_DOWNLOAD_FG,
            activebackground=T.BTN_DOWNLOAD_ACTIVE,
            command=self._on_download,
            **btn_cfg,
        ).grid(row=0, column=0, padx=10, pady=6)

        tk.Button(
            btn_frame,
            text="📝  ดึง Caption + แปล + พากย์",
            bg=T.BTN_CAPTION_BG,
            fg=T.BTN_CAPTION_FG,
            activebackground=T.BTN_CAPTION_ACTIVE,
            command=self._on_caption,
            **btn_cfg,
        ).grid(row=0, column=1, padx=10, pady=6)

        tk.Button(
            btn_frame,
            text="🤖  สรุปด้วย AI",
            bg=T.BTN_SUMMARIZE_BG,
            fg=T.BTN_SUMMARIZE_FG,
            activebackground=T.BTN_SUMMARIZE_ACTIVE,
            command=self._on_summarize,
            **btn_cfg,
        ).grid(row=0, column=2, padx=10, pady=6)

    def _build_log_area(self) -> None:
        self.log_panel = LogPanel(self.root, self.root)
        self.log_panel.pack(pady=16, padx=50, fill="both", expand=True)

    def _build_footer(self) -> None:
        tk.Label(
            self.root,
            text="GtsAlpha Caption Pro  •  รองรับ YouTube & X/Twitter (สาธารณะ)  •  AI ผ่าน Ollama",
            font=T.FONT_FOOTER,
            bg=T.BG,
            fg=T.TEXT_FOOTER,
        ).pack(side="bottom", pady=12)

    # ── Helpers ──────────────────────────────────────────────────────────────

    def log(self, msg: str) -> None:
        """Thread-safe logging to the log panel."""
        self.log_panel.log(msg)

    def _get_url(self) -> Optional[str]:
        """Return the trimmed URL from the entry, or show a warning and return None."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("กรุณากรอก URL", "วางลิงก์ YouTube หรือ X/Twitter ก่อนครับ")
            return None
        try:
            validate_url(url)
        except InvalidURLError as exc:
            messagebox.showwarning("URL ไม่ถูกต้อง", str(exc))
            return None
        return url

    def _pick_output_dir(self) -> None:
        chosen = filedialog.askdirectory(initialdir=self.output_dir)
        if chosen:
            self.output_dir = chosen
            self._dir_label.configure(text=chosen)
            self.log(f"เปลี่ยนโฟลเดอร์บันทึกเป็น: {chosen}")

    def _run_in_thread(self, target) -> None:  # type: ignore[no-untyped-def]
        threading.Thread(target=target, daemon=True).start()

    # ── Button callbacks ─────────────────────────────────────────────────────

    def _on_download(self) -> None:
        url = self._get_url()
        if not url:
            return

        def run() -> None:
            try:
                download_video(url, output_dir=self.output_dir, log_fn=self.log)
                messagebox.showinfo(
                    "สำเร็จ",
                    f"ดาวน์โหลดวิดีโอเสร็จสมบูรณ์\nไฟล์อยู่ใน: {self.output_dir}",
                )
            except Exception as e:
                self.log(f"ดาวน์โหลดล้มเหลว: {e}")
                messagebox.showerror(
                    "ผิดพลาด",
                    f"ดาวน์โหลดไม่สำเร็จ\n{e}\n\nโปรดตรวจสอบว่าเป็นวิดีโอสาธารณะ",
                )

        self._run_in_thread(run)

    def _on_caption(self) -> None:
        url = self._get_url()
        if not url:
            return

        def run() -> None:
            try:
                result = caption.extract_and_save(
                    url, output_dir=self.output_dir, log_fn=self.log
                )
                tts.generate_speech_for_video(
                    result["th_text"],
                    result["video_id"],
                    output_dir=self.output_dir,
                    log_fn=self.log,
                )
                messagebox.showinfo(
                    "สำเร็จ",
                    "สร้างไฟล์ .srt (EN/TH) และเสียงพากย์ (.mp3) เรียบร้อยแล้ว",
                )
            except InvalidURLError as e:
                self.log(f"URL ไม่ถูกต้อง: {e}")
                messagebox.showerror("URL ไม่ถูกต้อง", str(e))
            except Exception as e:
                self.log(f"เกิดข้อผิดพลาด: {e}")
                messagebox.showerror("ผิดพลาด", str(e))

        self._run_in_thread(run)

    def _on_summarize(self) -> None:
        url = self._get_url()
        if not url:
            return

        selected_model = self.model_var.get().strip()
        if not selected_model:
            messagebox.showwarning("กรุณาเลือกโมเดล", "เลือกโมเดล AI ก่อนกดสรุปครับ")
            return

        def run() -> None:
            try:
                self.log("กำลังดึงคำบรรยายเพื่อสรุป...")
                video_id = extract_video_id(url)
                transcript = caption.fetch_transcript(video_id)
                en_text = caption.transcript_to_plain_text(transcript)
                th_text = translate_text(en_text)

                summary = summarizer.summarize(
                    th_text, model=selected_model, log_fn=self.log
                )
                self.log(f"สรุปจาก {selected_model}:\n{summary}")
                messagebox.showinfo(
                    f"สรุปจาก {selected_model}",
                    summary[:500] + ("..." if len(summary) > 500 else ""),
                )
            except InvalidURLError as e:
                self.log(f"URL ไม่ถูกต้อง: {e}")
                messagebox.showerror("URL ไม่ถูกต้อง", str(e))
            except ConnectionError:
                self.log(f"ไม่พบ Ollama กรุณารัน: ollama run {selected_model}")
                messagebox.showerror(
                    "ไม่พบ Ollama",
                    f"โปรดติดตั้งและรัน Ollama ก่อน\nคำสั่ง: ollama run {selected_model}",
                )
            except Exception as e:
                self.log(f"เกิดข้อผิดพลาด: {e}")
                messagebox.showerror("ผิดพลาด", str(e))

        self._run_in_thread(run)

    def _refresh_models(self) -> None:
        self.log("กำลังตรวจสอบโมเดลที่ติดตั้งใน Ollama...")

        def run() -> None:
            models = summarizer.fetch_models()
            self.root.after(0, self._update_model_combo, models)

        self._run_in_thread(run)

    def _update_model_combo(self, models: list[str]) -> None:
        self.model_combo["values"] = models
        current = self.model_var.get()
        if current not in models:
            self.model_var.set(models[0] if models else "gemma2:9b")
        count = len(models)
        if models == list(DEFAULT_MODELS):
            self.log(f"Ollama ไม่ตอบสนอง — แสดงรายการโมเดลที่แนะนำ ({count} รายการ)")
        else:
            self.log(f"พบโมเดลที่ติดตั้งแล้ว {count} รายการ ✓")

    # ── Run ──────────────────────────────────────────────────────────────────

    def run(self) -> None:
        """Start the Tk main loop."""
        self.root.mainloop()
