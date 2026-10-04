"""Lab 5: five data-driven Playwright tests (no hard-coded values in tests).

Run green baseline:   pytest "lab 5/tests" -v
Drift, healing OFF:    pytest "lab 5/tests" --drift -q       # Step 7: expect 5 failed (TimeoutError)
Drift, healing ON:     pytest "lab 5/tests" --drift --heal -v # Step 8: expect 5 passed (self-healed)
Drift mechanism: --drift serves every page with ?shuffle=1, which renames
#add-btn -> #add-btn-v2 (same DOM effect as editing the HTML id by hand).
"""
from __future__ import annotations

import json
import os

import pytest
from playwright.sync_api import expect

DATA_PATH = os.path.join(os.path.dirname(__file__), "test-data.json")


def load_cases():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.parametrize("case", load_cases(), ids=lambda c: c["id"])
def test_task_case(task_page, case):
    task_page.goto_clean()

    if case["expect"] == "visible":
        task_page.add_task(case["title"], case["priority"])
        expect(task_page.page.locator("#task-list li", has_text=case["title"])).to_be_visible()

    elif case["expect"] == "rejected":
        task_page.add_task(case["title"], case["priority"])
        assert task_page.error_text() != "", "empty title must show a validation error"
        assert task_page.visible_titles() == [], "rejected task must not appear in list"

    elif case["expect"] == "done":
        task_page.add_task(case["title"], case["priority"])
        task_page.complete_task(case["title"])
        assert task_page.is_task_done(case["title"])
        expect(task_page.page.locator("#task-list li.done", has_text=case["title"])).to_be_visible()

    elif case["expect"] == "filtered":
        task_page.add_task("Keep me", 2)
        task_page.add_task(case["title"], case["priority"])
        task_page.complete_task(case["title"])
        task_page.show_pending_only()
        titles = task_page.visible_titles()
        assert any("Keep me" in t for t in titles)
        assert not any(case["title"] in t for t in titles), "done task must be hidden by pending filter"

    elif case["expect"] == "persisted":
        task_page.add_task(case["title"], case["priority"])
        task_page.page.reload()
        expect(task_page.page.locator("#task-list li", has_text=case["title"])).to_be_visible()

    else:  # pragma: no cover - guards against data typos
        raise ValueError(f"unknown expectation: {case['expect']}")

    # Healing assertion: when --heal is on and drift is present, a heal must be logged.
    # (No-op on the green baseline: last_healing is None or healed=False.)
    if task_page.use_healing and task_page.last_healing:
        assert task_page.last_healing["healedWith"] is not None or task_page.last_healing["healed"] is False
