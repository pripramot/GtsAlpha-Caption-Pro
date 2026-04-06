"""GUI theme constants — colours, fonts, and style tokens."""

from __future__ import annotations

# ── Colour palette ──────────────────────────────────────────────────────────
ACCENT = "#00d4ff"
BG = "#0a0f1c"
CARD = "#121a2e"
TEXT_LIGHT = "#e2e8f0"
TEXT_DIM = "#94a3b8"
TEXT_FOOTER = "#64748b"
TEXT_SUBTITLE = "#cbd5e1"
LOG_FG = "#4ade80"

ENTRY_BG = "#1e2937"
ENTRY_FG = "#f1f5f9"
BTN_REFRESH_BG = "#1e3a5f"
LOG_BG = "#0f172a"

BTN_DOWNLOAD_BG = ACCENT
BTN_DOWNLOAD_FG = "#0a0f1c"
BTN_DOWNLOAD_ACTIVE = "#38bdf8"

BTN_CAPTION_BG = "#22c55e"
BTN_CAPTION_FG = "#0a0f1c"
BTN_CAPTION_ACTIVE = "#4ade80"

BTN_SUMMARIZE_BG = "#a855f7"
BTN_SUMMARIZE_FG = "#ffffff"
BTN_SUMMARIZE_ACTIVE = "#c084fc"

# ── Font families ───────────────────────────────────────────────────────────
FONT_FAMILY = "TH Sarabun New"
FONT_MONO = "Consolas"

FONT_TITLE = (FONT_FAMILY, 44, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 18)
FONT_BODY = (FONT_FAMILY, 13)
FONT_BODY_BOLD = (FONT_FAMILY, 13, "bold")
FONT_ENTRY = (FONT_FAMILY, 14)
FONT_SMALL = (FONT_FAMILY, 11)
FONT_FOOTER = (FONT_FAMILY, 10)
FONT_BTN = (FONT_FAMILY, 13, "bold")
FONT_LOG = (FONT_MONO, 11)
FONT_LOG_LABEL = (FONT_FAMILY, 12, "bold")
FONT_REFRESH = (FONT_FAMILY, 12)
