"""Text-to-speech wrapper around gTTS."""

from __future__ import annotations

import os
from typing import Callable, Optional

from gtts import gTTS


def generate_speech(
    text: str,
    output_path: str,
    lang: str = "th",
    log_fn: Optional[Callable[[str], None]] = None,
) -> str:
    """Generate a speech audio file from text.

    Args:
        text: The text to convert to speech.
        output_path: File path for the output MP3.
        lang: Language code for TTS (default ``"th"``).
        log_fn: Optional logging callback.

    Returns:
        The output file path.
    """
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    if log_fn:
        log_fn("สร้างเสียงพากย์ .mp3 สำเร็จ ✓")
    return output_path


def generate_speech_for_video(
    th_text: str,
    video_id: str,
    output_dir: str = ".",
    log_fn: Optional[Callable[[str], None]] = None,
) -> str:
    """Convenience: generate TH speech for a given video ID.

    Args:
        th_text: Thai text to speak.
        video_id: YouTube video ID (used in filename).
        output_dir: Output directory.
        log_fn: Optional logging callback.

    Returns:
        Path to the generated MP3 file.
    """
    output_path = os.path.join(output_dir, f"TH_{video_id}.mp3")
    return generate_speech(th_text, output_path, lang="th", log_fn=log_fn)
