# Lab 5 Plan: Test Automation Framework & Self-Healing Locators

**Stack:** Playwright + Node.js (tests) + minimal Flask web UI (target app)
**Duration:** 2.5 hrs | **Week 5 | COMP 441**

## 1. Context / Findings

- Current sample app (`app/cli.py`, `app/tasks.py`) is CLI-only, no HTML/UI to test.
- Repo is Python-only (`requirements.txt` = `pytest`); no `package.json`, no Playwright yet.
- `docker` is NOT installed on this machine, and Healenium is Selenium-only.
  Real `docker-compose up healenium` is therefore not possible with the chosen stack.
- Decision: implement **Playwright-native self-healing** (fallback-locator engine)
  instead of Healenium, and explicitly document that substitution in the final report.

## 2. Proposed Structure (all new under `lab 5/`)

```text
lab 5/
  plan.md                        # this file
  web/app.py                     # minimal Flask UI wrapping app/tasks.py (add/complete/list)
  tests/package.json
  tests/playwright.config.js
  tests/pages/TaskPage.js        # Page Object Model
  tests/task.spec.js             # 5x data-driven tests
  tests/test-data.json           # (or .csv) - no hard-coded values in tests
  tests/utils/healing.js         # self-healing locator wrapper + healing-report.json logger
  before-after-failure-report.md
  healing-report.md + screenshots/
```

## 3. Execution Plan (~2.5 hr)

### Step 1 — Sample web app (30 min)

Build a single Flask page wrapping the existing `app/tasks.py` logic:

- Routes: `GET /` (list), `POST /add`, `POST /complete`.
- Elements with stable selectors for the POM:
  `#task-input`, `#add-btn`, `#task-list li`, `#filter-pending`.
- Serve on `http://localhost:5000` for Playwright.

Maps to lab Step 1 (project init prerequisite: a target page exists).

### Step 2 — Playwright + Node init (15 min)

```powershell
Set-Location "lab 5/tests"
npm init -y
npm init playwright@latest
npx playwright install chromium
```

Maps to lab Step 1.

### Step 3 — Page Object Model (25 min)

Create `tests/pages/TaskPage.js` encapsulating all locators + actions.
No asserts in the page object:

- `goto()`
- `addTask(title, priority)`
- `completeTask(title)`
- `getTasks()`

Locators live ONLY here, so UI drift breaks one place. Maps to lab Step 2.

### Step 4 — Five data-driven tests (30 min)

- `tests/test-data.json`: 5+ rows (title, priority, expected).
- `tests/task.spec.js` reads the file and loops, covering e.g.:
  1. add-valid task appears in list
  2. add-empty title rejected
  3. complete-task marks done
  4. pending-filter hides done tasks
  5. persistence — reload keeps tasks
- Run suite, confirm 5/5 green. Maps to lab Steps 3-4.

### Step 5 — Drift simulation (15 min)

Intentionally rename ONE locator in `web/app.py`, e.g.:

- `id="add-btn"` -> `id="add-btn-v2"` (or class change).

Re-run suite with healing **disabled**.
Record which tests fail and why (`TimeoutError`, strict-mode violation).

Maps to lab Steps 6-7.

### Step 6 — Self-healing run (25 min)

Re-run same suite with `tests/utils/healing.js` enabled:

```js
async heal(page, primary, fallbacks, name)
// try primary first, else iterate fallbacks, log decision
```

Fallback chain example for Add button:
`#add-btn` -> `getByRole('button', {name: 'Add'})` -> `getByText('Add')` -> `css .btn-add` -> `xpath //button[contains(@class,'add')]`.

Each attempt logs `{ broken, healedWith, confidence }` to `healing-report.json`
(mimics Healenium dashboard/logs).

Record success rate + any wrong-element heals. Maps to lab Step 8.

### Step 7 — Deliverables (10 min)

1. `lab 5/tests/` source (POM, 5 tests, data file).
2. `before-after-failure-report.md` — before/after table for the locator change.
3. `healing-report.md` + `screenshots/` — healing table + short analysis:

| Test | Before | After (no heal) | After (heal) | Healed locator | Wrong element? |

Maps to lab Step 9.

## 4. Trade-off / Marking Risk

Steps 5/8 will state: "Healenium skipped — incompatible with Playwright + no
Docker on this host; equivalent fallback-locator engine used."

If the instructor strictly requires a Healenium dashboard screenshot,
switch to the alternative: `Selenium + Python + Docker Desktop`.

## 5. Status

- [x] Plan written
- [ ] Step 1: web UI
- [ ] Step 2: Playwright init
- [ ] Step 3: POM
- [ ] Step 4: 5 tests green
- [ ] Step 5: drift + failure report
- [ ] Step 6: healing run + healing report
