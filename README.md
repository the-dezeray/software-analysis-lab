# Task Manager (Lab 1 Sample Repository)

A tiny in-memory/file-backed task manager used as the seeded sample project
for Module Lab 1 (Environment Setup & Manual Defect Hunting).

## Setup
```
pip install -r requirements.txt
```

## Run
```
python -m app.cli
```

## Test
```
pytest
```

## Where my labs are

I keep each lab in its own folder in the repo root:

- `lab 1/` - my test results (`test-results.md`). 4 passed, 2 failed.
- `lab 2/` - my radon + lint results (`cyclometic-complexity-results.md`,
  `maintainability-index-results.md`, `lint_report_before.txt`,
  `lint_report_after.txt`).
- `lab 3/` - my EP/BVA tables, my 11 test cases, and my AI vs mine
  comparison (`tables.md`, `test-cases.md`, `comparison.md`).
- `lab 4/` - my requirements, my 10 test cases, my RTM, my test plan for
  FR-03, my defect log (DEF-01, DEF-02), and my AI comparison
  (`requirements.md`, `test-cases.md`, `rtm.md`, `test-plan.md`,
  `defect-log.md`, `ai-comparison.md`).
- `lab 5/` - my Playwright framework + self-healing run (`web/`, `tests/`,
  `before-after-failure-report.md`, `healing-report.md`, `reflection.md`).
- `lab 6/` - my AI vs manual coverage work (`assistant.md`, `prompts.md`,
  `comparison.md`, `coverage-*.txt`).
- `lab 7/` - my mutation testing work (`README.md`, three mutation reports,
  `surviving-mutants.md`, `final-results.md`, `reflection.md`, and raw
  logs/HTML reports under `reports/`).
- `lab 9/` - my exploratory testing session (`charter.md`, `ai-ideas.md`,
  `session-notes.md`, `session-report.md`).

## Extra tests I added

I did not delete the starter tests. I added mine next to them:

- `tests/test_discount_lab3.py` - my 11 Lab 3 cases for
  `calculate_discount`. I got 7 passed, 4 failed (1, 8, 10, 11 DID NOT RAISE).
- `tests/test_ai_lab6.py` - 8 AI-generated tests for Lab 6.
- `tests/test_manual_lab6.py` - my 10 manual tests for Lab 6
  (`remove_task`, `find_task_by_title`, `format_task_report`).
- `tests/test_lab7_mutation_killers.py` - my 3 targeted tests that kill the
  surviving AI-suite mutants from Lab 7.
- `lab 5/tests/` - my 5 Playwright tests with POM
  (`test_tasks.py` + `test-data.json` + `pages/task_page.py` +
  `utils/healing.py`). Baseline is 5 passed (~2.4 s).

Run what I ran:

```
pytest tests/test_discount_lab3.py -v
pytest tests/test_ai_lab6.py tests/test_manual_lab6.py --cov=app --cov-report=term-missing
pytest tests/test_ai_lab6.py tests/test_lab7_mutation_killers.py -q
pytest "lab 5/tests" -v
pytest "lab 5/tests" --drift -q
pytest "lab 5/tests" --drift --heal -v
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py" --tests-dir tests --simple-output --no-progress
```

Lab 7 needs a green baseline, so I fixed the Lab 6 `format_task_report`
TypeError in `app/storage.py` before running `mutmut`. The Lab 6 coverage
files remain the historical record of the pre-fix failing code. My other
defect fixes are still only written up in `lab 4/defect-log.md` (iterate all
tasks, `if not tasks: return 0`). What I actually changed:

- Added the test files above, no starter test touched.
- Fixed `app/storage.py` line 14 (`str(task["id"])`) for the Lab 7 baseline.
- Added `pyproject.toml` with the `[tool.mutmut]` configuration.
- Added `lab 5/web/index.html` - my static copy of the task app for
  Playwright to hit. Drift is via `--drift` (`add-btn` -> `add-btn-v2`).
- Added `lab 5/tests/utils/healing.py` - my fallback engine instead of
  Healenium (I have no Docker and Healenium is Selenium-only).
- Added all my lab write-ups listed above.
