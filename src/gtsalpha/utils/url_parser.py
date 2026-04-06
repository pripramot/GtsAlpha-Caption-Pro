"""URL parsing and validation utilities for YouTube and social media video links."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse


class InvalidURLError(Exception):
    """Raised when a URL cannot be parsed into a valid video ID."""


# Patterns that match common YouTube URL formats
_YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
_TWITTER_DOMAINS = {"twitter.com", "www.twitter.com", "x.com", "www.x.com"}
_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(url: str) -> str:
    """Extract a YouTube video ID from various URL formats.

    Supported formats:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        - https://www.youtube.com/shorts/VIDEO_ID

    Args:
        url: A YouTube video URL.

    Returns:
        The 11-character YouTube video ID.

    Raises:
        InvalidURLError: If the URL is not a recognised YouTube format or the
            extracted ID does not look valid.
    """
    url = url.strip()
    if not url:
        raise InvalidURLError("URL is empty")

    parsed = urlparse(url)

    # Ensure the URL has a scheme for proper parsing
    if not parsed.scheme:
        parsed = urlparse(f"https://{url}")

    hostname = (parsed.hostname or "").lower()

    # youtu.be/VIDEO_ID
    if hostname == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0].split("?")[0]
        return _validate_video_id(video_id, url)

    # youtube.com/watch?v=VIDEO_ID
    if hostname in _YOUTUBE_DOMAINS:
        if parsed.path in ("/watch", "/watch/"):
            qs = parse_qs(parsed.query)
            ids = qs.get("v", [])
            if ids:
                return _validate_video_id(ids[0], url)

        # /embed/VIDEO_ID or /shorts/VIDEO_ID or /v/VIDEO_ID
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] in ("embed", "shorts", "v", "live"):
            return _validate_video_id(parts[1], url)

    raise InvalidURLError(
        f"Cannot extract a YouTube video ID from: {url}"
    )


def is_supported_url(url: str) -> bool:
    """Return True if the URL belongs to a supported platform (YouTube or X/Twitter)."""
    url = url.strip()
    if not url:
        return False
    parsed = urlparse(url if "://" in url else f"https://{url}")
    hostname = (parsed.hostname or "").lower()
    return hostname in (_YOUTUBE_DOMAINS | _TWITTER_DOMAINS)


def validate_url(url: str) -> str:
    """Validate and normalise a URL string.

    Returns the stripped URL if it looks valid, otherwise raises InvalidURLError.
    """
    url = url.strip()
    if not url:
        raise InvalidURLError("URL is empty")

    parsed = urlparse(url if "://" in url else f"https://{url}")
    if not parsed.hostname:
        raise InvalidURLError(f"Invalid URL: {url}")

    return url


def _validate_video_id(video_id: str, original_url: str) -> str:
    """Check that a candidate video ID has the expected format."""
    video_id = video_id.strip()
    if _VIDEO_ID_RE.match(video_id):
        return video_id
    raise InvalidURLError(
        f"Extracted ID '{video_id}' does not look like a valid YouTube video ID "
        f"(from URL: {original_url})"
    )
