# Lab 4 - Test cases (my design, 10 cases)

Each requirement has at least one test case. "Maps to" = existing pytest test in the repo.

| TC ID | Requirement | Input / Steps | Expected | Maps to | Test Level |
|-------|-------------|---------------|----------|---------|------------|
| TC-01 | FR-01 | `add_task([], "Write report")` | 1 task, title matches, done=False | `test_add_task_creates_task` | Unit |
| TC-02 | FR-02 | add "Write report", `complete_task(tasks, 1)`; also `complete_task(tasks, 99)` | True + done=True; False for 99 | `test_complete_task_marks_done` | Unit |
| TC-03 | FR-03 | add "Task A", add "Task B", `get_pending_tasks(tasks)` | 2 pending (A and B) | `test_get_pending_tasks_includes_first_task` | Unit |
| TC-04 | FR-03 | add A, add B, complete A, `get_pending_tasks(tasks)` | 1 pending (B only) | new (no pytest yet) | Integration |
| TC-05 | FR-04 | `average_priority([])` | 0 | `test_average_priority_of_empty_list` | Unit |
| TC-06 | FR-04 | tasks with priorities 1, 2, 3 | 2.0 | new (no pytest yet) | Unit |
| TC-07 | FR-05 | add "Write report", `find_task_by_title(tasks, "Write report")` + missing title | task returned; None for missing | new (no pytest yet) | Unit |
| TC-08 | FR-06 | add A, add B, `remove_task(tasks, 1)` | A gone, B remains | new (no pytest yet) | Unit |
| TC-09 | FR-07 | `calculate_discount(100, True)` and `(100, False)` | 80 and 100 | `test_calculate_discount_for_premium_user` / `_regular_user` | Unit |
| TC-10 | FR-07 | `(-1, True)`, `(10000.01, False)`, `(100, 1)`, `("100", True)` | ValueError / ValueError / TypeError / TypeError | lab 3 `test_case1/8/10/9` | Unit |

## Results (`pytest -v`, 02/10/2026)

- Pass: TC-01, TC-02, TC-09 (all lab-3 valid-range discount cases too).
- Fail: TC-03 (returns 1 task, skips index 0), TC-05 (ZeroDivisionError), TC-10 invalid inputs (DID NOT RAISE).
- Not run: TC-04, TC-06, TC-07, TC-08 (designed here, not automated yet).
