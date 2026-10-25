# Mutation report - combined suite

Command:

```powershell
$env:PYTHONIOENCODING = "utf-8"
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py tests/test_manual_lab6.py" `
  --tests-dir tests --simple-output --no-progress
```

Baseline: 18 tests, 18 passed after the `format_task_report` fix.

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

Combining the suites does not raise the target score above the manual suite,
because the manual suite already kills all 15 target mutants. It does make the
suite stronger overall: the AI tests add independent checks, and the combined
run still kills the 26 mutants the manual suite killed.

## Evidence

- Raw run: `reports/combined-run.txt`
- Survivors: `reports/combined-survivors.txt`
- HTML report: `reports/html-combined/index.html`
- Mutation cache: `reports/combined-cache.sqlite`
