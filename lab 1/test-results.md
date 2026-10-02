## Test Results

```
tests/test_tasks.py::test_add_task_creates_task               PASSED
tests/test_tasks.py::test_complete_task_marks_done            PASSED
tests/test_tasks.py::test_get_pending_tasks_includes_first_task  FAILED
tests/test_tasks.py::test_average_priority_of_empty_list       FAILED
tests/test_tasks.py::test_calculate_discount_for_premium_user  PASSED
tests/test_tasks.py::test_calculate_discount_for_regular_user  PASSED
```

**Summary: 2 failed, 4 passed.**

| Test | Result | Root Cause |
|------|--------|------------|
| `test_get_pending_tasks_includes_first_task` | FAILED | Defect #3 — `range(1, len(tasks))` skips the task at index 0; returns 1 instead of 2 |
| `test_average_priority_of_empty_list` | FAILED | Defect #4 — `ZeroDivisionError: division by zero` at `app/tasks.py:59` |
| Remaining 4 tests | PASSED | — |
