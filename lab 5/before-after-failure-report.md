# Before / After Failure Report — Lab 5 Locator Drift

**Target:** `lab 5/web/index.html` (static UI mirroring `app/tasks.py`) · **Framework:** Python Playwright + POM (`lab 5/tests`)
**Drift injected:** `id="add-btn"` → `id="add-btn-v2"` (via `?shuffle=1` hook, same effect as editing the HTML)

## Result table (5 data-driven cases from `tests/test-data.json`)

| Test | Before (baseline) | After drift, healing OFF | After drift, healing ON (`--heal`) |
|---|---|---|---|
| add-valid | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS — healed via `role:button[name=Add]` |
| add-empty | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS — healed |
| complete | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS — healed |
| pending-filter | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS — healed |
| persistence | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS — healed |

Baseline verified: `pytest "lab 5/tests" -v` → **5 passed**; `pytest "lab 5/tests" -v --heal` → **5 passed**.
Drift probe verified: healing OFF raises `TimeoutError` (screenshot `screenshots/failure-no-heal.png`);
healing ON completes the add and logs the decision (screenshot `screenshots/healed.png`).

## Why everything fails without healing

The POM (`tests/pages/task_page.py`) is the single source of truth for locators, so one
renamed id breaks every test that clicks Add — 5/5 red from a one-line UI change. This is the
brittleness the lab asks us to demonstrate (cf. plan.md Steps 5–7). No test logic changed;
only the locator did, which is why a fallback-locator engine fixes all five at once.
