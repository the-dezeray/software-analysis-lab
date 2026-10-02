# Lab 6 - Prompts used for AI generation

Same prompt shape for each function: pasted the function's code plus its
docstring, then asked for unit tests. Example (for `remove_task`):

> Here is a Python function with its docstring:
> ```python
> def remove_task(tasks, task_id):
>     """Remove a task by id."""
>     for i in range(len(tasks)):
>         if tasks[i]["id"] == task_id:
>             del tasks[i]
>             break
> ```
> Write pytest unit tests for this function. Use `add_task` to build test data.

(Same pattern for `find_task_by_title` and `format_task_report`,
showing each function's own code + docstring.)

First-run result: imports and syntax were correct, no fixes needed.
2 of the 8 generated tests fail at runtime - not a test bug, they expose a
real app bug (`format_task_report` crashes, see comparison.md). Left as-is.
