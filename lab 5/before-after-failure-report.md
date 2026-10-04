# Before / After Failure Report — Lab 5 Locator Drift (manual Step 7)

**Target:** `lab 5/web/index.html` (static UI mirroring `app/tasks.py`) · **Framework:** Python Playwright + POM (`lab 5/tests`)
**Drift injected:** `id="add-btn"` → `id="add-btn-v2"` — via the `--drift` flag, which serves every page
with `?shuffle=1` (the JS hook renames the id on load; identical DOM effect to editing the attribute
by hand, and reversible so the green baseline stays intact).

## Result table (5 data-driven cases from `tests/test-data.json`)

| Test | Before (baseline) | After drift, healing OFF (`--drift`) | After drift, healing ON (`--drift --heal`, see healing report) |
|---|---|---|---|
| add-valid | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS |
| add-empty | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS |
| complete | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS |
| pending-filter | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS |
| persistence | PASS | FAIL — `TimeoutError` on `#add-btn` | PASS |

Actual runs (from the repo root):

```powershell
pytest "lab 5/tests" -v              # baseline → 5 passed (≈2.4 s)
pytest "lab 5/tests" --drift -q      # Step 7, healing OFF → 5 failed in 157.38 s
pytest "lab 5/tests" --drift --heal -v  # Step 8, healing ON → 5 passed in 11.82 s
```

- Baseline: **5 passed** (≈2.4 s).
- Drift, no healing: `pytest "lab 5/tests" --drift -q` → **5 failed in 157.38 s** (above), every failure
  `playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded … waiting for locator("#add-btn")`.
- Drift, healing: `pytest "lab 5/tests" --drift --heal -v` → **5 passed in 11.82 s** (above).

## Why everything fails without healing

The POM (`tests/pages/task_page.py`) is the single source of truth for locators, so one
renamed id breaks every test that clicks Add — 5/5 red from a one-line UI change, each burning a
full 30 s Playwright timeout (hence 157 s total). This is the brittleness the lab asks us to
demonstrate (manual Steps 6–7). No test logic changed; only the locator did, which is why a
fallback-locator engine fixes all five at once — compare 11.82 s healed vs 157 s failed.
