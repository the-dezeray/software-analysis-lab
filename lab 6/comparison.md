# Lab 6 - Comparison table + verdict

Command for all three runs: `pytest <files> --cov=app --cov-report=term-missing`
(pytest-cov 7.1.0; full outputs in coverage-ai.txt / coverage-manual.txt /
coverage-combined.txt). Assertion counts via `Select-String -Pattern "assert"`.

| Run | Tests (pass/fail) | Coverage TOTAL | app/tasks.py | app/storage.py | Assertions | Assertion strength |
|-----|-------------------|----------------|--------------|----------------|------------|--------------------|
| AI-only (`test_ai_lab6.py`) | 8 (6/2) | 45% | 51% | 56% | 9 | Weak |
| Manual-only (`test_manual_lab6.py`) | 10 (8/2) | 45% | 51% | 56% | 19 | Strong |
| Combined | 18 (14/4) | 45% | 51% | 56% | 28 | Mixed |

(The 2+2+4 failures are all the same real app bug: `format_task_report`
crashes with `TypeError` on any non-empty list, `app/storage.py:14`.
Missing line 15 - `lines.append` - is never reached because of it.)

## Weak vs strong examples

- Weak (AI): `assert isinstance(report, str)` and `assert len(tasks) == 1`.
  The first says nothing about content; the second passes even if the WRONG
  task was deleted.
- Strong (manual): `assert tasks == [task_b]` plus id/title checks (fails if
  the wrong task is removed), `assert format_task_report(tasks) ==
  "Task #1: Task A\nTask #2: Task B"` (pins the exact contract),
  duplicate-title first-match and case-sensitivity checks the AI never tried.

## Verdict: where AI was weakest

Same coverage (45% three times - merging added zero lines), but the AI suite
checks roughly half as much per test (9 vs 19 assertions) and only the
happy path: no duplicates, no case-sensitivity, never asserts WHICH task
survives `remove_task`, never pins the report format. Its empty-list report
test (`== ""`) even passes despite the crash bug, giving false confidence.
Useful as a first draft and a crash-finder, not as a correctness check.

## Reflection: high coverage with weak assertions?

Yes - concrete example: `test_ai_report_empty_list` passes (`format_task_report([])`
returns `""` without touching the buggy line), so the AI suite reports the
reporting feature partly green while EVERY non-empty call crashes. And
`test_ai_remove_deletes_task` only asserts `len(tasks) == 1` - it would still
pass if the function deleted Task B instead of Task 1. Coverage says the lines
ran; only the manual suite's exact-equality assertions say they ran correctly.
