# Healing Report — Lab 5 Self-Healing Locators (manual Step 8)

**Engine:** `lab 5/tests/utils/healing.py` — `heal(page, primary, fallbacks, name)` tries the primary
locator first, then walks the fallback chain and appends each decision to `tests/healing-report.json`.

> **Healenium substitution (manual Step 5):** Healenium is Selenium-only and this host has no Docker,
> so `docker-compose up healenium` plus the proxy setup is impossible here, and the chosen stack is
> Playwright (permitted: "Playwright or Selenium, Node.js or Python"). The fallback-locator engine
> above is the documented equivalent: ordered fallbacks + a per-decision log standing in for the
> Healenium dashboard/logs. `tests/healing-report.json` is the machine-readable log; this file is
> the written analysis; `screenshots/` holds the visual evidence (no dashboard screenshot exists
> because no Healenium backend was run).

**Fallback chain for the Add button:** `#add-btn` → `role:button[name=Add]` → `text:Add` →
`css:.btn-add` → `testid:add-btn` → `xpath://button[contains(@class,'add')]` (confidence 1.0 → 0.5 down the chain).

## Healing table (actual `--drift --heal` run: 5 passed in 11.82 s)

| Test | Before | After (no heal) | After (heal) | Healed locator | Wrong element? |
|---|---|---|---|---|---|
| add-valid | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (conf. 0.95) | No — task appeared in list |
| add-empty | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (conf. 0.95) | No — validation error shown, list empty |
| complete | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (conf. 0.95) | No — task marked done |
| pending-filter | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` ×2 (conf. 0.95) | No — done task hidden by filter |
| persistence | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (conf. 0.95) | No — task survived reload |

Raw log: `lab 5/tests/healing-report.json` — **6 entries** (pending-filter adds two tasks, so it heals
twice), all `broken: #add-btn` → `healedWith: role:button[name=Add]`, `confidence: 0.95`,
`~1525 ms` each (one primary-visibility timeout before fallback kicks in). Screenshots:
`screenshots/failure-no-heal.png`, `screenshots/healed.png`.

## Short analysis

- **Success rate: 5/5 tests (6/6 healed lookups), 0 wrong-element heals.** The role+accessible-name
  fallback is unambiguous on this page, so deeper fallbacks (text/CSS/XPath) were never reached.
- **Cost:** ~1.5 s per healed lookup vs a 30 s timeout-and-fail without healing (11.82 s healed suite
  vs 157 s red suite). Zero cost on the green baseline — the primary hits, nothing is logged.
- **Flakiness note:** the page also ships `?flaky=1` (random 0–1200 ms render delay, `window.__FLAKY__` /
  `window.__RENDER_DELAY__`) so timing flakiness can be demoed: hard `wait_for_timeout` sleeps flake
  while Playwright web-first asserts (`expect(...).to_be_visible()`) with auto-retry stay green.
  Locator healing and auto-waiting are complementary — healing fixes *where*, waiting fixes *when*.
