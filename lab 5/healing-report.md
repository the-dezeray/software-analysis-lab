# Healing Report — Lab 5 Self-Healing Locators

**Engine:** `lab 5/tests/utils/healing.py` — `heal(page, primary, fallbacks, name)` tries the primary
locator first, then walks the fallback chain and appends each decision to `tests/healing-report.json`
(local stand-in for the Healenium dashboard; see `plan.md` §4 for why Healenium itself was skipped:
Selenium-only + no Docker on this host).

**Fallback chain for the Add button:** `#add-btn` → `role:button[name=Add]` → `text:Add` →
`css:.btn-add` → `testid:add-btn` → `xpath://button[contains(@class,'add')]` (confidence 1.0 → 0.5 down the chain).

## Healing table

| Test | Before | After (no heal) | After (heal) | Healed locator | Wrong element? |
|---|---|---|---|---|---|
| add-valid | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (conf. 0.95) | No — task "drift probe (P2)" appeared in list |
| add-empty | PASS | FAIL (`TimeoutError`) | PASS | same chain | No |
| complete | PASS | FAIL (`TimeoutError`) | PASS | same chain | No |
| pending-filter | PASS | FAIL (`TimeoutError`) | PASS | same chain | No |
| persistence | PASS | FAIL (`TimeoutError`) | PASS | same chain | No |

Raw log: `lab 5/tests/healing-report.json` (1 entry from the drift probe: `broken: #add-btn`,
`healedWith: role:button[name=Add]`, `confidence: 0.95`, `~1525 ms` — the ~1.5 s is the
primary-visibility timeout before fallback kicks in). Screenshots: `screenshots/failure-no-heal.png`,
`screenshots/healed.png`.

## Short analysis

- **Success rate:** 5/5 drifted tests recover with `--heal`; 0 wrong-element heals observed (role+name
  is unambiguous on this page; text/CSS fallbacks were not needed).
- **Cost:** ~1.5 s extra per healed lookup (one visibility timeout). Acceptable for a drifted locator;
  zero cost on the green baseline (primary hits, nothing logged).
- **Flakiness note:** the page also ships `?flaky=1` (random 0–1200 ms render delay, `window.__FLAKY__` /
  `window.__RENDER_DELAY__`) so timing flakiness can be demoed: hard `wait_for_timeout` sleeps flake
  while Playwright web-first asserts (`expect(...).to_be_visible()`) with auto-retry stay green.
  Locator healing and auto-waiting are complementary — healing fixes *where*, waiting fixes *when*.
