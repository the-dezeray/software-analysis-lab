

## Identified Defects

| ID | File | Line | Description | Severity |
|----|------|------|-------------|----------|
| 1 | app/tasks.py | 23 | `tags=[]` mutable default argument — every task created without explicit tags shares the same list object; mutating one task's tags corrupts others | High |
| 2 | app/tasks.py | 26 | `id = len(tasks) + 1` — after a task is removed, the next generated ID collides with still-existing IDs, producing duplicate task IDs | Medium |
| 3 | app/tasks.py | 48 | `range(1, len(tasks))` — off-by-one loop that skips index 0 (the first task is never considered) | High |
| 4 | app/tasks.py | 59 | `total / len(tasks)` — no empty-list guard; dividing by zero raises `ZeroDivisionError` | High |
| 5 | app/tasks.py | 62–66 | `find_task_by_title` — no explicit return when no match is found; falls off the end and silently returns `None` | Medium |
| 6 | app/tasks.py | 69–74 | `remove_task` — returns `None` whether or not the task existed; callers cannot tell if removal succeeded | Low |
| 7 | app/tasks.py | 79 | `if is_premium == True` — non-idiomatic comparison to `True` (PEP 8 E712) | Low |
| 8 | app/tasks.py | 11 | `f = open(...)` without a `with` block — file handle is never closed; corrupt or `null` JSON flows through with no validation that the result is a list | Medium |
| 9 | app/storage.py | 11 | `"Task #" + task["id"] + ": "` — string concatenation with an integer → `TypeError` at runtime | High |
| 10 | app/storage.py | 4 | Hardcoded `API_KEY` secret committed in source (TODO even admits it should be an env var) | High |
| 11 | app/storage.py | 26 | `build_query` — SQL built via naive string concatenation → SQL injection vulnerability | High |
| 12 | app/storage.py | 18–21 | `days_until_due` — `datetime.now()` includes time-of-day; truncation to `.days` can be off by one depending on the current time | Low |




