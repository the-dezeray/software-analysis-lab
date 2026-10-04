"""Page Object Model for the Lab 5 task-manager page.

All selectors live ONLY here. Tests must never hard-code a locator —
they call these methods. Healing is opt-in via ``use_healing=True``.
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.healing import add_button_fallbacks, heal


class TaskPage:
    def __init__(self, page, base_url: str, use_healing: bool = False, default_query: str = ""):
        self.page = page
        self.base_url = base_url
        self.use_healing = use_healing
        self.default_query = default_query
        self.last_healing = None  # record dict from the most recent heal() call

    # -- navigation ------------------------------------------------------
    def goto(self, query: str = "") -> None:
        q = query or self.default_query
        q = q if (not q or q.startswith("?")) else f"?{q}"
        self.page.goto(f"{self.base_url}/{q}")

    def goto_clean(self, query: str = "") -> None:
        """Navigate with a cleared localStorage (test isolation)."""
        self.goto(query)
        self.page.evaluate("localStorage.clear()")
        self.goto(query)

    # -- locators (single source of truth) --------------------------------
    def _add_button(self):
        if not self.use_healing:
            return self.page.locator("#add-btn")
        locator, record = heal(
            self.page,
            lambda: self.page.locator("#add-btn"),
            add_button_fallbacks(self.page),
            name="add-button",
        )
        self.last_healing = record
        return locator

    # -- actions ----------------------------------------------------------
    def add_task(self, title: str, priority: int = 2) -> None:
        self.page.locator("#task-input").fill(title)
        self.page.locator("#priority-input").select_option(str(priority))
        self._add_button().click()

    def complete_task(self, title: str) -> None:
        self.page.locator(f"[data-complete='{title}']").click()

    def show_pending_only(self) -> None:
        self.page.locator("#filter-pending").click()

    def show_all(self) -> None:
        self.page.locator("#filter-all").click()

    def clear_all(self) -> None:
        self.page.locator("#clear-btn").click()

    # -- observations -----------------------------------------------------
    def visible_titles(self):
        return self.page.locator("#task-list li").all_inner_texts()

    def error_text(self) -> str:
        return self.page.locator("#error").inner_text().strip()

    def is_task_done(self, title: str) -> bool:
        li = self.page.locator(f"#task-list li[data-title='{title}']")
        cls = li.get_attribute("class") or ""
        return "done" in cls
