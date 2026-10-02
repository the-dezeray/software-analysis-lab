# Lab 4 - Mini test plan (IEEE 829 style) for FR-03

Selected requirement: FR-03 - "The system shall return all pending (not-done)
tasks, including every task in the list." Chosen because TC-03 currently fails
(real defect DEF-01), so entry/exit criteria actually matter here.

## 1. Scope
Features to test: `get_pending_tasks()` in `app/tasks.py` plus its use in
`app/cli.py` (pending count on the summary report). Out of scope: task
creation, completion, persistence, discount logic.

## 2. Entry criteria
- `app/tasks.py` builds without errors; `pytest tests/test_tasks.py -k pending` is collectable.
- Test data helper (`add_task`) available; cases TC-03 and TC-04 reviewed.

## 3. Test items and approach
- TC-03 (unit): two tasks added, both pending -> expect 2 back.
- TC-04 (integration): complete one task, list pending -> expect only the other.
- Re-run after any fix to `get_pending_tasks()` (regression: full `test_tasks.py`).

## 4. Exit criteria
- TC-03 and TC-04 both pass; no open severity-major+ defects against FR-03.
- DEF-01 is Closed (fix verified); full suite has no new failures vs. baseline
  (6 failed / 11 passed on 02/10/2026 - only pre-existing Lab 3 discount + DEF-01/DEF-02 failures allowed).
- Suspension: stop and re-plan if the function signature changes or the CLI stops calling it.

## 5. Current verdict
Not exiting yet: TC-03 fails (off-by-one, DEF-01 open), TC-04 not automated.
