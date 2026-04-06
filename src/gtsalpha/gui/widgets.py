"""Reusable GUI widgets — thread-safe log panel."""

from __future__ import annotations

import datetime
import tkinter as tk
from tkinter import scrolledtext

from gtsalpha.gui.theme import ACCENT, CARD, FONT_LOG, FONT_LOG_LABEL, LOG_BG, LOG_FG


class LogPanel(tk.LabelFrame):
    """A scrollable, read-only log panel that can be updated from any thread."""

    def __init__(self, parent: tk.Widget, root: tk.Tk, **kwargs) -> None:
        super().__init__(
            parent,
            text="  สถานะการทำงาน  ",
            font=FONT_LOG_LABEL,
            bg=CARD,
            fg=ACCENT,
            padx=12,
            pady=8,
            **kwargs,
        )
        self._root = root
        self._text = scrolledtext.ScrolledText(
            self,
            height=14,
            font=FONT_LOG,
            bg=LOG_BG,
            fg=LOG_FG,
            relief="flat",
            state="disabled",
        )
        self._text.pack(padx=8, pady=8, fill="both", expand=True)

    def log(self, msg: str) -> None:
        """Append a timestamped message to the log (thread-safe)."""
        self._root.after(0, self._append, msg)

    def _append(self, msg: str) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self._text.configure(state="normal")
        self._text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self._text.see(tk.END)
        self._text.configure(state="disabled")
