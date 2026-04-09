"""Tests for gtsalpha.core.translator — translation with retries."""

import pytest

from gtsalpha.core.translator import translate_text


class TestTranslateText:
    def test_successful_translation(self, mocker):
        mock_translator = mocker.Mock()
        mock_translator.return_value.translate.return_value = "สวัสดี"
        mocker.patch("gtsalpha.core.translator.GoogleTranslator", mock_translator)

        result = translate_text("Hello", source="en", target="th")
        assert result == "สวัสดี"
        mock_translator.assert_called_once_with(source="en", target="th")

    def test_retries_on_failure(self, mocker):
        mock_translator_cls = mocker.Mock()
        # Fail once, then succeed
        mock_translator_cls.return_value.translate.side_effect = [
            Exception("network error"),
            "สวัสดี",
        ]
        mocker.patch("gtsalpha.core.translator.GoogleTranslator", mock_translator_cls)
        mocker.patch("gtsalpha.core.translator.time.sleep")

        result = translate_text("Hello", max_retries=2)
        assert result == "สวัสดี"
        assert mock_translator_cls.return_value.translate.call_count == 2

    def test_raises_after_exhausting_retries(self, mocker):
        mock_translator_cls = mocker.Mock()
        mock_translator_cls.return_value.translate.side_effect = Exception("fail")
        mocker.patch("gtsalpha.core.translator.GoogleTranslator", mock_translator_cls)
        mocker.patch("gtsalpha.core.translator.time.sleep")

        with pytest.raises(Exception, match="fail"):
            translate_text("Hello", max_retries=2)

    def test_default_languages(self, mocker):
        mock_translator_cls = mocker.Mock()
        mock_translator_cls.return_value.translate.return_value = "result"
        mocker.patch("gtsalpha.core.translator.GoogleTranslator", mock_translator_cls)

        translate_text("text")
        mock_translator_cls.assert_called_with(source="en", target="th")
