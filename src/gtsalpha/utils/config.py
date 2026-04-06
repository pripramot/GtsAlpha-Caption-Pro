"""Application-wide constants and configuration."""

from __future__ import annotations

# Ollama local API endpoint
OLLAMA_API: str = "http://localhost:11434"

# Default popular Ollama models shown when the server is unreachable
DEFAULT_MODELS: list[str] = [
    "gemma2:9b",
    "gemma2:2b",
    "llama3:8b",
    "llama3:70b",
    "mistral:7b",
    "phi3:mini",
    "qwen2:7b",
]

# Network timeouts (seconds)
OLLAMA_TAGS_TIMEOUT: int = 5
OLLAMA_GENERATE_TIMEOUT: int = 120
NETWORK_MAX_RETRIES: int = 3
NETWORK_BACKOFF_FACTOR: float = 1.0

# AI summarization prompt template
SUMMARIZE_PROMPT_TEMPLATE: str = "สรุปเนื้อหาต่อไปนี้เป็นภาษาไทยให้กระชับ:\n\n{text}"
SUMMARIZE_TEXT_LIMIT: int = 4000

# yt-dlp default options
YTDLP_FORMAT: str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
