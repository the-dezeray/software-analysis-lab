# Mutation report - manual suite only

Command:

```powershell
$env:PYTHONIOENCODING = "utf-8"
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_manual_lab6.py" `
  --tests-dir "tests/test_manual_lab6.py" --simple-output --no-progress
```

Baseline: 10 manual tests, 10 passed after the `format_task_report` fix.

## Result

| Scope | Killed | Survived | Suspicious | Timeout | Mutation score |
|-------|--------|----------|------------|---------|----------------|
| Three target functions | 15 | 0 | 0 | 0 | **15 / 15 = 100.0%** |
| All mutants in both files | 26 | 39 | 0 | 0 | 26 / 65 = 40.0% |

Per target function:

| Function | Killed | Total | Score |
|----------|--------|-------|-------|
| `find_task_by_title` | 2 | 2 | 100.0% |
| `remove_task` | 3 | 3 | 100.0% |
| `format_task_report` | 10 | 10 | 100.0% |

The manual suite kills every target mutant. It also kills more unrelated
mutants than the AI suite because its `add_task` assertions pin the exact task
dictionary, which catches mutants in `add_task` that the AI suite misses.

## Evidence

- Raw run: `reports/manual-only-run.txt`
- Survivors: `reports/manual-only-survivors.txt`
- HTML report: `reports/html-manual-only/index.html`
- Mutation cache: `reports/manual-only-cache.sqlite`
