# Lab 5 - healing report

Engine I wrote: `lab 5/tests/utils/healing.py` - `heal(page, primary, fallbacks, name)`.
It tries my primary locator first and then walks the fallback chain. Every
decision goes to `tests/healing-report.json`.

> Healenium note: I could not run Healenium here. It is Selenium-only and I
> have no Docker on this machine, so I could not do `docker-compose up healenium`.
> My stack is Playwright (allowed: "Playwright or Selenium"). So I wrote the
> fallback engine above instead. `healing-report.json` is my log and this file
> is my analysis. I have screenshots in `screenshots/` but no dashboard
> screenshot because I never ran a Healenium backend.

Chain I used for the Add button: `#add-btn` -> `role:button[name=Add]` ->
`text:Add` -> `css:.btn-add` -> `testid:add-btn` -> `xpath://button[contains(@class,'add')]`.

## Healing table (`--drift --heal`: 5 passed in 11.82 s)

| Test | Before | After (no heal) | After (heal) | Healed with | Wrong element? |
|---|---|---|---|---|---|
| add-valid | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (0.95) | No - task showed in list |
| add-empty | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (0.95) | No - error shown, list empty |
| complete | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (0.95) | No - task marked done |
| pending-filter | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` x2 (0.95) | No - done task hidden |
| persistence | PASS | FAIL (`TimeoutError`) | PASS | `role:button[name=Add]` (0.95) | No - task survived reload |

Log: `lab 5/tests/healing-report.json` - 6 entries (pending-filter adds two
tasks so it heals twice). All are `broken: #add-btn` -> `healedWith:
role:button[name=Add]`, confidence 0.95, ~1525 ms each.
Screenshots: `screenshots/failure-no-heal.png`, `screenshots/healed.png`.

## Reproduce (from repo root)

```powershell
pytest "lab 5/tests" -v              # baseline -> 5 passed (~2.4 s)
pytest "lab 5/tests" --drift -q      # healing OFF -> 5 failed
pytest "lab 5/tests" --drift --heal -v  # healing ON -> 5 passed in 11.82 s
```

## Short analysis

I healed 5/5 tests (6/6 lookups) and I got 0 wrong-element heals. My
role+name fallback matched straight away so I never reached the text/CSS/XPath
fallbacks.

It costs me ~1.5 s per heal vs 30 s timeout-and-fail without healing
(11.82 s healed vs 157 s red). On the green baseline it costs nothing
because my primary hits and nothing is logged.

Flaky note: I also added `?flaky=1` (random 0-1200 ms delay). My hard sleeps
flake there but my Playwright `expect(...).to_be_visible()` asserts stay
green. So healing fixes *where* and auto-waiting fixes *when* for me.
