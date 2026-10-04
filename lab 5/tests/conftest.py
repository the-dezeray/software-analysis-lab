"""Pytest fixtures: local HTTP server + Playwright page + TaskPage."""
from __future__ import annotations

import functools
import http.server
import os
import sys
import threading

import pytest
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(__file__))

WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web"))


@pytest.fixture(scope="session")
def base_url():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WEB_DIR)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    server.shutdown()


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture()
def page(browser):
    ctx = browser.new_context()
    pg = ctx.new_page()
    yield pg
    ctx.close()


@pytest.fixture()
def task_page(page, base_url, request):
    from pages.task_page import TaskPage

    use_healing = request.config.getoption("--heal", default=False)
    drift = request.config.getoption("--drift", default=False)
    return TaskPage(page, base_url, use_healing=use_healing,
                    default_query="?shuffle=1" if drift else "")


def pytest_addoption(parser):
    parser.addoption("--heal", action="store_true", help="enable self-healing locators")
    parser.addoption("--drift", action="store_true",
                     help="serve the drifted UI (?shuffle=1 renames #add-btn -> #add-btn-v2)")
