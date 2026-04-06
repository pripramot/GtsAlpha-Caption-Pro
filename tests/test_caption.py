"""Tests for gtsalpha.core.caption — SRT generation and transcript helpers."""

from gtsalpha.core.caption import (
    _format_srt_time,
    create_srt,
    transcript_to_plain_text,
)

# ── _format_srt_time ────────────────────────────────────────────────────────


class TestFormatSrtTime:
    def test_zero_seconds(self):
        assert _format_srt_time(0) == "0:00:00,000"

    def test_one_hour(self):
        assert _format_srt_time(3600) == "1:00:00,000"

    def test_mixed_time(self):
        assert _format_srt_time(3661) == "1:01:01,000"

    def test_under_a_minute(self):
        assert _format_srt_time(42) == "0:00:42,000"


# ── transcript_to_plain_text ────────────────────────────────────────────────


class TestTranscriptToPlainText:
    def test_joins_text_fields(self):
        items = [
            {"text": "Hello", "start": 0, "duration": 1},
            {"text": "world", "start": 1, "duration": 1},
        ]
        assert transcript_to_plain_text(items) == "Hello world"

    def test_empty_list(self):
        assert transcript_to_plain_text([]) == ""

    def test_single_item(self):
        items = [{"text": "solo", "start": 0, "duration": 1}]
        assert transcript_to_plain_text(items) == "solo"


# ── create_srt (no translation) ─────────────────────────────────────────────


class TestCreateSrt:
    SAMPLE_TRANSCRIPT = [
        {"text": "Hello", "start": 0, "duration": 2},
        {"text": "World", "start": 2, "duration": 3},
    ]

    def test_basic_srt_format(self):
        srt = create_srt(self.SAMPLE_TRANSCRIPT, translate=False)
        lines = srt.strip().split("\n")
        # First block: index, timestamp, text
        assert lines[0] == "1"
        assert "-->" in lines[1]
        assert lines[2] == "Hello"

    def test_segment_numbering(self):
        srt = create_srt(self.SAMPLE_TRANSCRIPT, translate=False)
        assert "1\n" in srt
        assert "2\n" in srt

    def test_timestamps_correct(self):
        srt = create_srt(self.SAMPLE_TRANSCRIPT, translate=False)
        assert "0:00:00,000 --> 0:00:02,000" in srt
        assert "0:00:02,000 --> 0:00:05,000" in srt

    def test_empty_transcript(self):
        srt = create_srt([], translate=False)
        assert srt == ""

    def test_translated_srt_calls_translator(self, mocker):
        mock_translate = mocker.patch("gtsalpha.core.caption.translate_text", return_value="สวัสดี")
        srt = create_srt(self.SAMPLE_TRANSCRIPT, translate=True)
        assert mock_translate.call_count == 2
        assert "สวัสดี" in srt
