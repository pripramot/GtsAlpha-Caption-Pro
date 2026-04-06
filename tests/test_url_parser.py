"""Tests for gtsalpha.utils.url_parser."""

import pytest

from gtsalpha.utils.url_parser import (
    InvalidURLError,
    extract_video_id,
    is_supported_url,
    validate_url,
)

# ── extract_video_id ─────────────────────────────────────────────────────────


class TestExtractVideoId:
    """Tests for the extract_video_id function."""

    def test_standard_watch_url(self):
        assert extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_watch_url_with_extra_params(self):
        assert (
            extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42&list=PLtest")
            == "dQw4w9WgXcQ"
        )

    def test_short_url(self):
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_short_url_with_query(self):
        assert extract_video_id("https://youtu.be/dQw4w9WgXcQ?t=10") == "dQw4w9WgXcQ"

    def test_embed_url(self):
        assert extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_shorts_url(self):
        assert extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_mobile_url(self):
        assert extract_video_id("https://m.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_no_scheme(self):
        assert extract_video_id("youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_live_url(self):
        assert extract_video_id("https://www.youtube.com/live/dQw4w9WgXcQ") == "dQw4w9WgXcQ"

    def test_empty_url_raises(self):
        with pytest.raises(InvalidURLError, match="empty"):
            extract_video_id("")

    def test_whitespace_only_raises(self):
        with pytest.raises(InvalidURLError, match="empty"):
            extract_video_id("   ")

    def test_non_youtube_url_raises(self):
        with pytest.raises(InvalidURLError, match="Cannot extract"):
            extract_video_id("https://vimeo.com/12345678")

    def test_twitter_url_raises(self):
        """X/Twitter URLs are supported for download but not for transcript extraction."""
        with pytest.raises(InvalidURLError, match="Cannot extract"):
            extract_video_id("https://x.com/user/status/123456")

    def test_invalid_video_id_raises(self):
        with pytest.raises(InvalidURLError, match="does not look like"):
            extract_video_id("https://youtu.be/short")


# ── is_supported_url ─────────────────────────────────────────────────────────


class TestIsSupportedUrl:
    """Tests for the is_supported_url function."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=abc",
            "https://youtu.be/abc",
            "https://m.youtube.com/watch?v=abc",
            "https://twitter.com/user/status/123",
            "https://x.com/user/status/123",
        ],
    )
    def test_supported_urls(self, url):
        assert is_supported_url(url) is True

    @pytest.mark.parametrize(
        "url",
        [
            "",
            "   ",
            "https://vimeo.com/123",
            "https://dailymotion.com/video/abc",
            "not-a-url",
        ],
    )
    def test_unsupported_urls(self, url):
        assert is_supported_url(url) is False


# ── validate_url ─────────────────────────────────────────────────────────────


class TestValidateUrl:
    """Tests for the validate_url function."""

    def test_valid_url_returned_stripped(self):
        assert validate_url("  https://youtube.com  ") == "https://youtube.com"

    def test_empty_url_raises(self):
        with pytest.raises(InvalidURLError, match="empty"):
            validate_url("")

    def test_url_without_scheme(self):
        # Should not raise — scheme is added internally for parsing
        result = validate_url("youtube.com/watch?v=abc")
        assert result == "youtube.com/watch?v=abc"
