# Final results - killer tests and improved mutation score

## New tests

Added `tests/test_lab7_mutation_killers.py`:

| Test | Survivor targeted | Assertion |
|------|-------------------|-----------|
| `test_kill_47_exact_task_prefix` | 47 | Report starts with `Task #1:` |
| `test_kill_51_exact_colon_separator` | 51 | Report equals `Task #1: Task A` |
| `test_kill_55_single_newline_between_tasks` | 55 | Two-task report equals `Task #1: Task A\nTask #2: Task B` |

Each test fails against its mutant and passes against the real code. The exact
two-task assertion also pins the separator between records, which is the
contract the AI suite never checked.

## Re-run - AI suite + killer tests

Command:

```powershell
$env:PYTHONIOENCODING = "utf-8"
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py tests/test_lab7_mutation_killers.py" `
  --tests-dir tests --simple-output --no-progress
```

| Scope | Before | After | Change |
|-------|--------|-------|--------|
| Target functions | 12 / 15 = 80.0% | **15 / 15 = 100.0%** | +20.0 points |
| All mutants | 17 / 65 = 26.2% | 20 / 65 = 30.8% | +4.6 points |

All three previously surviving target mutants (47, 51, 55) are now killed.

## Re-run - final combined suite + killer tests

Command:

```powershell
$env:PYTHONIOENCODING = "utf-8"
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py tests/test_manual_lab6.py tests/test_lab7_mutation_killers.py" `
  --tests-dir tests --simple-output --no-progress
```

Result: **15 / 15 target mutants killed = 100.0%**.
All-mutant result: 24 killed, 2 suspicious, 39 survived out of 65
(24 / 65 = 36.9% strict; the 2 suspicious mutants are unrelated `add_task`
mutants, not target functions).

The final target score is **100.0%**, up from the AI-only **80.0%**.

## Evidence

- AI + killers raw run: `reports/ai-plus-killers-run.txt`
- AI + killers HTML: `reports/html-ai-plus-killers/index.html`
- Final combined raw run: `reports/final-combined-run.txt`
- Final combined HTML: `reports/html-final-combined/index.html`
- Final combined survivors: `reports/final-combined-survivors.txt`

## Verification

```powershell
python -m pytest tests/test_ai_lab6.py tests/test_lab7_mutation_killers.py -q
python -m pytest tests/test_ai_lab6.py tests/test_manual_lab6.py tests/test_lab7_mutation_killers.py -q
```

Expected: 11 passed, then 21 passed.
