# Mutation report - AI-generated suite only

Command:

```powershell
$env:PYTHONIOENCODING = "utf-8"
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py" `
  --tests-dir "tests/test_ai_lab6.py" --simple-output --no-progress
```

Baseline: 8 AI tests, 8 passed after the `format_task_report` fix.

## Result

| Scope | Killed | Survived | Suspicious | Timeout | Mutation score |
|-------|--------|----------|------------|---------|----------------|
| Three target functions | 12 | 3 | 0 | 0 | **12 / 15 = 80.0%** |
| All mutants in both files | 17 | 48 | 0 | 0 | 17 / 65 = 26.2% |

Per target function:

| Function | Killed | Total | Score |
|----------|--------|-------|-------|
| `find_task_by_title` | 2 | 2 | 100.0% |
| `remove_task` | 3 | 3 | 100.0% |
| `format_task_report` | 7 | 10 | 70.0% |

The all-mutant score is low because `app/tasks.py` and `app/storage.py` also
contain functions the Lab 6 suites do not test (storage, pending tasks,
average priority, discount, due dates, query building). Those survivors are
outside the Lab 7 target scope.

## Surviving target mutants

All three are in `format_task_report`:

| ID | Mutation | Killed by manual suite? |
|----|----------|--------------------------|
| 47 | `"Task #"` -> `"XXTask #XX"` | Yes |
| 51 | `": "` -> `"XX: XX"` | Yes |
| 55 | `"\n".join(lines)` -> `"XX\nXX".join(lines)` | Yes |

Diffs are saved in `reports/ai-survivor-47.diff`, `reports/ai-survivor-51.diff`
and `reports/ai-survivor-55.diff`. The full survivor list is
`reports/ai-only-survivors.txt`.

## Evidence

- Raw run: `reports/ai-only-run.txt`
- Survivors: `reports/ai-only-survivors.txt`
- HTML report: `reports/html-ai-only/index.html`
- Mutation cache: `reports/ai-only-cache.sqlite`
