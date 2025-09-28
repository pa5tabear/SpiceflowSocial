"""Stable UID helpers for events."""
from __future__ import annotations

import hashlib
import re
from typing import Iterable


NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def normalize(text: str) -> str:
    text = text.strip().lower()
    text = NON_ALNUM_RE.sub(" ", text)
    return " ".join(text.split())


def generate_uid(*parts: Iterable[str | None]) -> str:
    """Generate a deterministic UID from the provided string parts."""

    flattened: list[str] = []
    for part in parts:
        if not part:
            continue
        if isinstance(part, str):
            flattened.append(normalize(part))
        else:
            flattened.append(normalize(str(part)))
    digest = hashlib.md5("|".join(flattened).encode("utf-8"))
    return digest.hexdigest()
