"""HTTP helper with light-weight conditional request caching."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

CACHE_DIR = Path("data/cache")
INDEX_FILE = CACHE_DIR / "index.json"


@dataclass
class CachedFetch:
    content: bytes
    headers: dict[str, Any]
    from_cache: bool
    status_code: int


def _load_index() -> dict[str, dict[str, Any]]:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {}


def _save_index(index: dict[str, dict[str, Any]]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, indent=2, sort_keys=True))


def fetch(url: str, *, timeout: float = 30.0, force_refresh: bool = False) -> CachedFetch:
    """Fetch a URL with conditional headers based on the cache index."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    index = _load_index()
    entry = index.get(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if entry and not force_refresh:
        if etag := entry.get("etag"):
            headers["If-None-Match"] = etag
        if last_modified := entry.get("last_modified"):
            headers["If-Modified-Since"] = last_modified
    filename = entry.get("filename") if entry else hashlib.sha256(url.encode("utf-8")).hexdigest()
    path = CACHE_DIR / filename

    with httpx.Client(follow_redirects=True, timeout=timeout) as client:
        response = client.get(url, headers=headers)

    if response.status_code == 304 and entry and path.exists():
        return CachedFetch(content=path.read_bytes(), headers=entry.get("response_headers", {}), from_cache=True, status_code=304)

    response.raise_for_status()
    path.write_bytes(response.content)
    index[url] = {
        "filename": filename,
        "etag": response.headers.get("ETag"),
        "last_modified": response.headers.get("Last-Modified"),
        "response_headers": dict(response.headers),
    }
    _save_index(index)
    return CachedFetch(content=response.content, headers=dict(response.headers), from_cache=False, status_code=response.status_code)
