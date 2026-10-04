"""Self-healing locator engine (Playwright-native Healenium substitute).

Rationale (documented in plan.md): Healenium is Selenium-only and this host
has no Docker, so a real ``docker-compose up healenium`` run is impossible.
This module provides the equivalent behaviour for Playwright: try the
primary locator first; on miss, walk an ordered fallback chain (role / text /
CSS / XPath) and log every decision to ``healing-report.json`` — the local
stand-in for the Healenium dashboard/logs.
"""
from __future__ import annotations

import json
import os
import time

REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "healing-report.json")


def _describe(locator) -> str:
    try:
        return str(locator)
    except Exception:  # pragma: no cover - defensive
        return repr(locator)


def _is_usable(locator, timeout_ms: int = 1500) -> bool:
    """Return True if at least one matching element becomes visible in time."""
    try:
        locator.first.wait_for(state="visible", timeout=timeout_ms)
        return True
    except Exception:
        return False


def heal(page, primary_factory, fallbacks, name: str, timeout_ms: int = 1500):
    """Resolve a locator with self-healing.

    Args:
        page: Playwright page.
        primary_factory: zero-arg callable returning the primary locator.
        fallbacks: list of ``(label, factory)`` tuples, tried in order.
        name: logical element name (e.g. ``"add-button"``) used in the log.
        timeout_ms: per-candidate visibility timeout.

    Returns:
        ``(locator, record)`` where record is
        ``{"element": name, "broken": <primary>, "healedWith": <label|None>,
          "healed": bool, "confidence": float, "ms": int}``.
        ``healed=False`` + ``healedWith=None`` means the primary worked.
    """
    started = time.time()
    primary = primary_factory()
    if _is_usable(primary, timeout_ms):
        ms = int((time.time() - started) * 1000)
        return primary, {
            "element": name,
            "broken": None,
            "healedWith": None,
            "healed": False,
            "confidence": 1.0,
            "ms": ms,
        }

    broken = _describe(primary)
    # Confidence decays down the chain: role (0.95) > text (0.85) > css (0.75) > xpath (0.65).
    for i, (label, factory) in enumerate(fallbacks):
        candidate = factory()
        if _is_usable(candidate, timeout_ms):
            ms = int((time.time() - started) * 1000)
            record = {
                "element": name,
                "broken": broken,
                "healedWith": label,
                "healed": True,
                "confidence": round(max(0.5, 0.95 - 0.1 * i), 2),
                "ms": ms,
            }
            log_healing(record)
            return candidate, record

    ms = int((time.time() - started) * 1000)
    record = {
        "element": name,
        "broken": broken,
        "healedWith": None,
        "healed": False,
        "confidence": 0.0,
        "ms": ms,
        "error": "all fallbacks exhausted",
    }
    log_healing(record)
    return primary, record  # caller will time out on use, preserving the real failure


def log_healing(record: dict, path: str = REPORT_PATH) -> None:
    """Append one healing decision to the JSON report file."""
    path = os.path.abspath(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(record)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_button_fallbacks(page):
    """Ordered fallback chain for the Add button (role > text > css > xpath)."""
    return [
        ("role:button[name=Add]", lambda: page.get_by_role("button", name="Add")),
        ("text:Add", lambda: page.get_by_text("Add", exact=True)),
        ("css:.btn-add", lambda: page.locator("css=.btn-add")),
        ("testid:add-btn", lambda: page.get_by_test_id("add-btn")),
        ("xpath://button[contains(@class,'add')]", lambda: page.locator("xpath=//button[contains(@class,'add')]")),
    ]
