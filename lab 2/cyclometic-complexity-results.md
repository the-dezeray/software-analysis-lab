# Cyclomatic Complexity Results

Command: `radon cc -s src/`

Note: No `src/` directory exists in this repo (source is in `app/`). `radon cc -s src/` returns empty. Below is the result for the actual source `app/` (`radon cc -s app/`), plus average.

## `radon cc -s app/`

```
app\cli.py
    F 6:0 main - A (1)
app\storage.py
    F 8:0 format_task_report - A (2)
    F 19:0 days_until_due - A (1)
    F 27:0 build_query - A (1)
app\tasks.py
    F 38:0 complete_task - A (3)
    F 47:0 get_pending_tasks - A (3)
    F 65:0 find_task_by_title - A (3)
    F 73:0 remove_task - A (3)
    F 8:0 load_tasks - A (2)
    F 23:0 add_task - A (2)
    F 56:0 average_priority - A (2)
    F 81:0 calculate_discount - A (2)
    F 17:0 save_tasks - A (1)
```

## `radon cc -s app/ --total-average`

```
app\cli.py
    F 6:0 main - A (1)
app\storage.py
    F 8:0 format_task_report - A (2)
    F 19:0 days_until_due - A (1)
    F 27:0 build_query - A (1)
app\tasks.py
    F 38:0 complete_task - A (3)
    F 47:0 get_pending_tasks - A (3)
    F 65:0 find_task_by_title - A (3)
    F 73:0 remove_task - A (3)
    F 8:0 load_tasks - A (2)
    F 23:0 add_task - A (2)
    F 56:0 average_priority - A (2)
    F 81:0 calculate_discount - A (2)
    F 17:0 save_tasks - A (1)

13 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.0)
```

All blocks rank A (low risk, complexity 1-3).
