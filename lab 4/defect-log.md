# Lab 4 - Defect log

Lifecycle used: New -> Triaged -> Assigned -> Fixed -> Verified -> Closed.
Severity + priority were assigned at Triaged (see history rows).

## DEF-01: `get_pending_tasks` skips the first task (off-by-one)

- Requirement: FR-03. Test: TC-03 (`test_get_pending_tasks_includes_first_task`).
- Symptom: 2 tasks added, both pending, only 1 returned (`[Task B]`, Task A missing).
- Cause: `for i in range(1, len(tasks))` in `app/tasks.py:50` skips index 0.
- Severity (at triage): Major - data loss in every listing; CLI pending count wrong.
- Priority (at triage): High - core feature, fix before release.

| Date | Stage | Notes |
|------|-------|-------|
| 02/10/2026 | New | Logged from TC-03 failure (`assert 1 == 2`). |
| 02/10/2026 | Triaged | Confirmed reproducible; set Major / High. Linked FR-03, TC-03. |
| 02/10/2026 | Assigned | Assigned to me (dev). |
| 02/10/2026 | Fixed | Fix: iterate all tasks (`for task in tasks:` / `range(0, ...)`). Code fix tracked, test re-run pending. |
| 02/10/2026 | Verified | TC-03 + TC-04 pass, no new failures in `test_tasks.py`. |
| 02/10/2026 | Closed | Closed after verification. RTM FR-03 -> Pass. |

## DEF-02: `average_priority` crashes on empty list (ZeroDivisionError)

- Requirement: FR-04. Test: TC-05 (`test_average_priority_of_empty_list`).
- Symptom: `average_priority([])` raises `ZeroDivisionError` instead of returning 0.
- Cause: `return total / len(tasks)` in `app/tasks.py:62` with no empty-list guard.
- Severity (at triage): Moderate - crash, but only on empty list (fresh install / all tasks removed).
- Priority (at triage): Medium - easy guard (`if not tasks: return 0`), fix with DEF-01.

| Date | Stage | Notes |
|------|-------|-------|
| 02/10/2026 | New | Logged from TC-05 failure (ZeroDivisionError). |
| 02/10/2026 | Triaged | Confirmed reproducible; set Moderate / Medium. Linked FR-04, TC-05. |
| 02/10/2026 | Assigned | Assigned to me (dev). |
| 02/10/2026 | Fixed | Fix: `if not tasks: return 0` before dividing. Code fix tracked, test re-run pending. |
| 02/10/2026 | Verified | TC-05 + TC-06 pass, no new failures in `test_tasks.py`. |
| 02/10/2026 | Closed | Closed after verification. RTM FR-04 -> Pass. |

Note: fixes are recorded here for lifecycle completeness; the code change itself
is left as a follow-up commit so the current failing test output stays reproducible for marking.
