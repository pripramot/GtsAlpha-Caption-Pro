"""Tests for gtsalpha.core.summarizer — Ollama API client."""

import pytest
import requests

from gtsalpha.core.summarizer import fetch_models, summarize
from gtsalpha.utils.config import DEFAULT_MODELS

# ── fetch_models ─────────────────────────────────────────────────────────────


class TestFetchModels:
    def test_returns_models_from_api(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": [{"name": "llama3:8b"}, {"name": "gemma2:9b"}]}
        mocker.patch("gtsalpha.core.summarizer.requests.get", return_value=mock_resp)

        result = fetch_models()
        assert result == ["llama3:8b", "gemma2:9b"]

    def test_returns_defaults_on_connection_error(self, mocker):
        mocker.patch(
            "gtsalpha.core.summarizer.requests.get",
            side_effect=requests.exceptions.ConnectionError,
        )
        result = fetch_models()
        assert result == list(DEFAULT_MODELS)

    def test_returns_defaults_on_empty_models(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"models": []}
        mocker.patch("gtsalpha.core.summarizer.requests.get", return_value=mock_resp)

        result = fetch_models()
        assert result == list(DEFAULT_MODELS)

    def test_returns_defaults_on_non_200(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 500
        mocker.patch("gtsalpha.core.summarizer.requests.get", return_value=mock_resp)

        result = fetch_models()
        assert result == list(DEFAULT_MODELS)


# ── summarize ────────────────────────────────────────────────────────────────


class TestSummarize:
    def test_successful_summarization(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "This is a summary."}
        mocker.patch("gtsalpha.core.summarizer.requests.post", return_value=mock_resp)

        result = summarize("some text", model="gemma2:9b")
        assert result == "This is a summary."

    def test_connection_error_propagates(self, mocker):
        mocker.patch(
            "gtsalpha.core.summarizer.requests.post",
            side_effect=requests.exceptions.ConnectionError("No Ollama"),
        )
        with pytest.raises(requests.exceptions.ConnectionError):
            summarize("some text", model="gemma2:9b")

    def test_non_200_raises_runtime_error(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 500
        mocker.patch("gtsalpha.core.summarizer.requests.post", return_value=mock_resp)
        mocker.patch("gtsalpha.core.summarizer.time.sleep")

        with pytest.raises(RuntimeError, match="status 500"):
            summarize("some text", model="gemma2:9b", max_retries=1)

    def test_truncates_long_text(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "ok"}
        mock_post = mocker.patch("gtsalpha.core.summarizer.requests.post", return_value=mock_resp)

        long_text = "x" * 10000
        summarize(long_text, model="test")

        # Verify the payload prompt uses truncated text
        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        assert len(payload["prompt"]) < 10000

    def test_log_fn_called(self, mocker):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"response": "ok"}
        mocker.patch("gtsalpha.core.summarizer.requests.post", return_value=mock_resp)

        log_messages = []
        summarize("text", model="test", log_fn=log_messages.append)
        assert len(log_messages) == 1
        assert "test" in log_messages[0]
