# Lab 7 - Mutation testing and suite effectiveness

Tool: `mutmut 2.4.0` (Python), configured in `pyproject.toml`.
Targets: the three functions from Lab 6.

| Function | File | Mutants |
|----------|------|---------|
| `find_task_by_title` | `app/tasks.py` | 2 |
| `remove_task` | `app/tasks.py` | 3 |
| `format_task_report` | `app/storage.py` | 10 |
| **Target total** | | **15** |

`mutmut` mutates the two files that contain the targets. The scores below are
reported for the 15 mutants inside the three target functions; the raw run
also contains mutants in unrelated functions (reported as "all mutants" for
context).

## Baseline fix

Mutation testing needs a green baseline. Before this lab, the Lab 6 suites had
4 failures caused by the real `format_task_report` bug (`"Task #" + task["id"]`
raises `TypeError`). I fixed that known bug in `app/storage.py` first:

```python
line = "Task #" + str(task["id"]) + ": " + task["title"]
```

The Lab 6 raw coverage files are still the historical record of the failing
code. After the fix, all 18 Lab 6 tests pass and mutation testing is valid.

## Scores

| Run | Tests | Target mutants killed | Target score | All-mutant result | All score |
|-----|-------|-----------------------|--------------|-------------------|-----------|
| AI-only (`test_ai_lab6.py`) | 8 | 12 / 15 | **80.0%** | 17 killed / 48 survived | 26.2% |
| Manual-only (`test_manual_lab6.py`) | 10 | 15 / 15 | **100.0%** | 26 killed / 39 survived | 40.0% |
| Combined | 18 | 15 / 15 | **100.0%** | 26 killed / 39 survived | 40.0% |
| AI + killer tests | 11 | 15 / 15 | **100.0%** | 20 killed / 45 survived | 30.8% |
| Final combined + killers | 21 | 15 / 15 | **100.0%** | 24 killed / 39 survived / 2 suspicious | 36.9% strict |

Mutation score = killed / (killed + survived + suspicious + timeout).
Skipped mutants are excluded; there were none.

## Files

- `mutation-report-ai-only.md` - AI-only report and survivors.
- `mutation-report-manual-only.md` - manual-only report.
- `mutation-report-combined.md` - combined report.
- `surviving-mutants.md` - analysis of the 3 AI-suite survivors.
- `final-results.md` - killer tests and improved score.
- `reflection.md` - coverage vs mutation score discussion.
- `reports/` - raw run logs, survivor lists, diffs, SQLite caches and HTML reports.
- `../tests/test_lab7_mutation_killers.py` - new targeted tests.

## Reproduce

```powershell
$env:PYTHONIOENCODING = "utf-8"

# AI only
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py" `
  --tests-dir tests --simple-output --no-progress

# Manual only
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_manual_lab6.py" `
  --tests-dir tests --simple-output --no-progress

# Combined
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py tests/test_manual_lab6.py" `
  --tests-dir tests --simple-output --no-progress

# Updated AI suite with the killer tests
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py tests/test_lab7_mutation_killers.py" `
  --tests-dir tests --simple-output --no-progress

# Final combined suite with the killer tests
Remove-Item -Force -Recurse .mutmut-cache
mutmut run --runner "python -m pytest -x -q tests/test_ai_lab6.py tests/test_manual_lab6.py tests/test_lab7_mutation_killers.py" `
  --tests-dir tests --simple-output --no-progress
```

`PYTHONIOENCODING=utf-8` is required on Windows: mutmut 2.4's spinner uses
Unicode glyphs that the default cp1252 console cannot encode. `mutmut results`
lists survivors, `mutmut show <id>` shows a diff, and `mutmut html` writes the
browsable report.
