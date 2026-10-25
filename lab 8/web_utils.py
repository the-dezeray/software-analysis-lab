"""Shared helpers for the Lab 8 Playwright scripts."""
from __future__ import annotations

import functools
import http.server
import threading
from contextlib import contextmanager
from pathlib import Path

WEB_DIR = Path(__file__).parent / "web"
STORE_KEY = "lab5.tasks"
TASKS = [
    {"id": 1, "title": "Write report", "priority": 2, "done": False},
    {"id": 2, "title": "Review slides", "priority": 1, "done": True},
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@contextmanager
def serve():
    handler = functools.partial(QuietHandler, directory=str(WEB_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()


def prepare_page(page, url: str) -> None:
    page.goto(url)
    page.evaluate("([key, tasks]) => localStorage.setItem(key, JSON.stringify(tasks))", [STORE_KEY, TASKS])
    page.reload()
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(150)
