"""Translation wrapper around deep-translator."""

from __future__ import annotations

import time
from typing import Optional

from deep_translator import GoogleTranslator

from gtsalpha.utils.config import NETWORK_BACKOFF_FACTOR, NETWORK_MAX_RETRIES


def translate_text(
    text: str,
    source: str = "en",
    target: str = "th",
    max_retries: int = NETWORK_MAX_RETRIES,
) -> str:
    """Translate *text* from *source* language to *target* language.

    Uses exponential backoff on transient failures.

    Args:
        text: The text to translate.
        source: Source language code (default ``"en"``).
        target: Target language code (default ``"th"``).
        max_retries: Maximum number of retry attempts.

    Returns:
        The translated text string.

    Raises:
        Exception: After exhausting retries.
    """
    last_error: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            return GoogleTranslator(source=source, target=target).translate(text)
        except Exception as exc:
            last_error = exc
            if attempt < max_retries - 1:
                time.sleep(NETWORK_BACKOFF_FACTOR * (2 ** attempt))
    raise last_error  # type: ignore[misc]
