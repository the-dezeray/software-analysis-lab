# Lab 5 - before / after failure report

Target I tested: `lab 5/web/index.html` (my static copy of `app/tasks.py`).
Framework I used: Python Playwright + POM (`lab 5/tests`).

Drift I injected: `id="add-btn"` -> `id="add-btn-v2"`. I did it with the
`--drift` flag which loads the page with `?shuffle=1` and renames the id
on load. Same effect as editing the HTML by hand, but I can turn it off
again so my green baseline stays.

## Result table (5 cases from `tests/test-data.json`)

| Test | Before | After drift, no heal (`--drift`) | After drift, heal on (`--drift --heal`) |
|---|---|---|---|
| add-valid | PASS | FAIL - `TimeoutError` on `#add-btn` | PASS |
| add-empty | PASS | FAIL - `TimeoutError` on `#add-btn` | PASS |
| complete | PASS | FAIL - `TimeoutError` on `#add-btn` | PASS |
| pending-filter | PASS | FAIL - `TimeoutError` on `#add-btn` | PASS |
| persistence | PASS | FAIL - `TimeoutError` on `#add-btn` | PASS |

Commands I ran (from repo root):

```powershell
pytest "lab 5/tests" -v                 # baseline -> 5 passed (~2.4 s)
pytest "lab 5/tests" --drift -q         # no healing -> 5 failed in 157.38 s
pytest "lab 5/tests" --drift --heal -v  # healing on -> 5 passed in 11.82 s
```

## Why everything fails without healing

I keep all my locators in one place (`tests/pages/task_page.py`), so one
renamed id breaks every test that clicks Add. I got 5/5 red from a one-line
change and each one burns a full 30 s timeout, that is why it took 157 s.
I did not change any test logic, only the locator, so a fallback locator
fixes all five at once.
