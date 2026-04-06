"""Video downloader using yt-dlp."""

from __future__ import annotations

import re
from typing import Callable

import yt_dlp

from gtsalpha.utils.config import YTDLP_FORMAT


def sanitize_filename(name: str) -> str:
    """Remove or replace characters that are unsafe for file names.

    Args:
        name: The raw file name (e.g. video title).

    Returns:
        A sanitised string safe for use as a file-system path component.
    """
    # Replace common path-separator and control characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    # Collapse multiple underscores / spaces
    sanitized = re.sub(r"[_\s]+", " ", sanitized).strip()
    # Limit length to avoid OS limits
    return sanitized[:200] if sanitized else "video"


def download_video(
    url: str,
    output_dir: str = ".",
    log_fn: Callable[[str], None] | None = None,
) -> str:
    """Download a video from YouTube or X/Twitter.

    Args:
        url: The video URL to download.
        output_dir: Directory to save the downloaded file.
        log_fn: Optional callback for progress logging.

    Returns:
        The path of the downloaded file.

    Raises:
        Exception: Propagates yt-dlp errors.
    """
    if log_fn:
        log_fn(f"กำลังดาวน์โหลดวิดีโอจาก: {url}")

    outtmpl = f"{output_dir}/%(title)s.%(ext)s"

    ydl_opts: dict = {
        "outtmpl": outtmpl,
        "format": YTDLP_FORMAT,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "restrictfilenames": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info) if info else ""

    if log_fn:
        log_fn("ดาวน์โหลดวิดีโอสำเร็จ ✓")

    return filename
