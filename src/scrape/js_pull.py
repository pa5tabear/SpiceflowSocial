"""Placeholder for JavaScript-rendered sources."""
from __future__ import annotations

from typing import Any


def pull(source: dict[str, Any], *, horizon_days: int) -> list[dict[str, Any]]:
    raise NotImplementedError(
        "JavaScript-rendered sources require Playwright. Run `run_all.py --include-js` after configuring a browser."
    )
