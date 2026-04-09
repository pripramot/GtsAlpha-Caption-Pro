"""YouTube caption extraction and SRT file generation."""

from __future__ import annotations

import os
from typing import Callable

from youtube_transcript_api import YouTubeTranscriptApi

from gtsalpha.core.translator import translate_text
from gtsalpha.utils.url_parser import extract_video_id


def fetch_transcript(
    video_id: str,
    languages: list[str] | None = None,
) -> list[dict]:
    """Fetch the transcript for a YouTube video.

    Args:
        video_id: The YouTube video ID.
        languages: Ordered list of preferred languages (default ``["en"]``).

    Returns:
        A list of transcript segment dicts with keys ``text``, ``start``, ``duration``.
    """
    if languages is None:
        languages = ["en"]
    return YouTubeTranscriptApi.get_transcript(video_id, languages=languages)


def transcript_to_plain_text(transcript: list[dict]) -> str:
    """Join transcript segments into a single plain-text string."""
    return " ".join(item["text"] for item in transcript)


def create_srt(
    items: list[dict],
    translate: bool = False,
    source_lang: str = "en",
    target_lang: str = "th",
) -> str:
    """Convert transcript items to SRT subtitle format.

    Args:
        items: Transcript segment dicts.
        translate: Whether to translate each segment.
        source_lang: Source language code for translation.
        target_lang: Target language code for translation.

    Returns:
        A string containing valid SRT content.
    """
    parts: list[str] = []
    for i, item in enumerate(items, start=1):
        start_ts = _format_srt_time(float(item["start"]))
        end_ts = _format_srt_time(float(item["start"]) + float(item["duration"]))
        text = (
            translate_text(item["text"], source=source_lang, target=target_lang)
            if translate
            else item["text"]
        )
        parts.append(f"{i}\n{start_ts} --> {end_ts}\n{text}\n")
    return "\n".join(parts)


def extract_and_save(
    url: str,
    output_dir: str = ".",
    log_fn: Callable[[str], None] | None = None,
) -> dict[str, str]:
    """Full pipeline: fetch transcript, translate, save SRT files and TTS.

    Args:
        url: YouTube video URL.
        output_dir: Directory for output files.
        log_fn: Optional logging callback.

    Returns:
        Dict with keys ``video_id``, ``en_srt``, ``th_srt``, ``en_text``, ``th_text``.
    """
    if log_fn:
        log_fn("กำลังดึงคำบรรยาย...")

    video_id = extract_video_id(url)
    if log_fn:
        log_fn(f"Video ID: {video_id}")

    transcript = fetch_transcript(video_id)
    en_text = transcript_to_plain_text(transcript)
    th_text = translate_text(en_text)

    th_srt_path = os.path.join(output_dir, f"TH_{video_id}.srt")
    en_srt_path = os.path.join(output_dir, f"EN_{video_id}.srt")

    th_srt_content = create_srt(transcript, translate=True)
    with open(th_srt_path, "w", encoding="utf-8") as f:
        f.write(th_srt_content)
    if log_fn:
        log_fn("สร้าง TH_.srt สำเร็จ ✓")

    en_srt_content = create_srt(transcript, translate=False)
    with open(en_srt_path, "w", encoding="utf-8") as f:
        f.write(en_srt_content)
    if log_fn:
        log_fn("สร้าง EN_.srt สำเร็จ ✓")

    return {
        "video_id": video_id,
        "en_srt": en_srt_path,
        "th_srt": th_srt_path,
        "en_text": en_text,
        "th_text": th_text,
    }


def _format_srt_time(total_seconds: float) -> str:
    """Format seconds as ``HH:MM:SS,mmm`` for SRT files."""
    total_ms = round(total_seconds * 1000)
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, ms = divmod(remainder, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"
