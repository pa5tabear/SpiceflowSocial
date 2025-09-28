"""Fetch and sanitize source content snippets for LLM prompts."""
from __future__ import annotations

from html.parser import HTMLParser
from typing import Any

from util.http_cache import fetch

MAX_CHARS = 5000


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self._skip_stack and self._skip_stack[-1] == tag:
            self._skip_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._skip_stack:
            return
        stripped = data.strip()
        if stripped:
            self._chunks.append(stripped)

    def get_text(self) -> str:
        return " ".join(self._chunks)


def fetch_context_for_source(source: dict[str, Any], *, max_chars: int = MAX_CHARS) -> str:
    """Fetch the source URL and return a cleaned text snippet for LLM prompts."""

    url = source.get("url")
    if not url:
        return ""

    try:
        response = fetch(url, timeout=20.0)
    except Exception:
        return ""

    snippet = _extract_text(response.content, max_chars=max_chars)
    return snippet


def _extract_text(content: bytes, *, max_chars: int) -> str:
    parser = _TextExtractor()
    try:
        parser.feed(content.decode("utf-8", errors="ignore"))
    except Exception:
        return ""
    text = parser.get_text()
    return text[:max_chars]


__all__ = ["fetch_context_for_source"]
