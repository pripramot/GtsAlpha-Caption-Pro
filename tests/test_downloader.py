"""Tests for gtsalpha.core.downloader — video download helpers."""

from gtsalpha.core.downloader import sanitize_filename


class TestSanitizeFilename:
    def test_removes_special_chars(self):
        assert sanitize_filename('file<>:"/\\|?*name') == "file name"

    def test_collapses_underscores_and_spaces(self):
        assert sanitize_filename("a___b   c") == "a b c"

    def test_strips_whitespace(self):
        assert sanitize_filename("  hello  ") == "hello"

    def test_truncates_long_names(self):
        long_name = "x" * 300
        result = sanitize_filename(long_name)
        assert len(result) <= 200

    def test_empty_string_returns_video(self):
        assert sanitize_filename("") == "video"

    def test_all_special_chars_returns_video(self):
        assert sanitize_filename("???***") == "video"

    def test_normal_title_unchanged(self):
        assert sanitize_filename("My Cool Video - 2024") == "My Cool Video - 2024"
