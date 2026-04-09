"""Ollama API client for AI-powered text summarization."""

from __future__ import annotations

import time
from typing import Callable

import requests

from gtsalpha.utils.config import (
    DEFAULT_MODELS,
    NETWORK_BACKOFF_FACTOR,
    NETWORK_MAX_RETRIES,
    OLLAMA_API,
    OLLAMA_GENERATE_TIMEOUT,
    OLLAMA_TAGS_TIMEOUT,
    SUMMARIZE_PROMPT_TEMPLATE,
    SUMMARIZE_TEXT_LIMIT,
)


def fetch_models(
    api_url: str = OLLAMA_API,
    timeout: int = OLLAMA_TAGS_TIMEOUT,
) -> list[str]:
    """Return list of locally installed Ollama model names.

    Falls back to DEFAULT_MODELS when the Ollama server is unreachable.

    Args:
        api_url: Base URL of the Ollama API.
        timeout: Request timeout in seconds.

    Returns:
        List of model name strings.
    """
    try:
        resp = requests.get(f"{api_url}/api/tags", timeout=timeout)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            if models:
                return models
    except Exception:
        pass
    return list(DEFAULT_MODELS)


def summarize(
    text: str,
    model: str,
    api_url: str = OLLAMA_API,
    timeout: int = OLLAMA_GENERATE_TIMEOUT,
    max_retries: int = NETWORK_MAX_RETRIES,
    log_fn: Callable[[str], None] | None = None,
) -> str:
    """Summarize text using an Ollama model.

    Args:
        text: The text to summarize (will be truncated to SUMMARIZE_TEXT_LIMIT).
        model: Name of the Ollama model to use.
        api_url: Base URL of the Ollama API.
        timeout: Request timeout in seconds.
        max_retries: Maximum retry attempts on transient failures.
        log_fn: Optional logging callback.

    Returns:
        The summary string from the model.

    Raises:
        requests.exceptions.ConnectionError: If Ollama is not running.
        RuntimeError: If the API returns a non-200 status.
    """
    truncated = text[:SUMMARIZE_TEXT_LIMIT]
    prompt = SUMMARIZE_PROMPT_TEMPLATE.format(text=truncated)
    payload = {"model": model, "prompt": prompt, "stream": False}

    if log_fn:
        log_fn(f"กำลังส่งข้อความให้ {model} สรุป (ต้องรัน Ollama อยู่)...")

    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = requests.post(f"{api_url}/api/generate", json=payload, timeout=timeout)
            if response.status_code == 200:
                return response.json().get("response", "")
            raise RuntimeError(f"Ollama returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise
        except Exception as exc:
            last_error = exc
            if attempt < max_retries - 1:
                time.sleep(NETWORK_BACKOFF_FACTOR * (2**attempt))

    raise last_error  # type: ignore[misc]
