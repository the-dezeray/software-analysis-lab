# Analysis of surviving mutants from the AI-only run

The AI suite produced 48 survivors overall. Only 3 are inside the Lab 7 target
functions, all in `format_task_report`. They are the meaningful ones for this
lab because the other 45 are in functions Lab 6 did not target.

## Survivor 47 - changed task prefix

Diff (`reports/ai-survivor-47.diff`):

```diff
-        line = "Task #" + str(task["id"]) + ": " + task["title"]
+        line = "XXTask #XX" + str(task["id"]) + ": " + task["title"]
```

The report still starts with a string containing the title, so the AI
assertions pass:

- `test_ai_report_returns_string` only checks `isinstance(report, str)`.
- `test_ai_report_contains_task_title` only checks `"Task A" in report`.

Neither assertion pins the prefix. The mutant changes the user-visible report
format from `Task #1: Task A` to `XXTask #XX1: Task A`, and both assertions
still succeed.

Killed by the new `test_kill_47_exact_task_prefix` (`startswith("Task #1:")`)
and by the manual suite's exact-string tests.

## Survivor 51 - changed colon separator

Diff (`reports/ai-survivor-51.diff`):

```diff
-        line = "Task #" + str(task["id"]) + ": " + task["title"]
+        line = "Task #" + str(task["id"]) + "XX: XX" + task["title"]
```

Same root cause: the AI suite checks the title and the type, not the exact
layout. `Task #1XX: XXTask A` is still a string and still contains `Task A`,
so both AI report tests pass.

Killed by the new `test_kill_51_exact_colon_separator` (exact equality) and by
the manual suite's `test_manual_report_single_task_exact_string`.

## Survivor 55 - changed newline join separator

Diff (`reports/ai-survivor-55.diff`):

```diff
-    return "\n".join(lines)
+    return "XX\nXX".join(lines)
```

The AI suite never checks the output of a multi-task report:

- `test_ai_report_contains_task_title` only looks for one title.
- `test_ai_report_empty_list` returns before `join` is called, so the empty
  list assertion is unaffected.

The mutant turns `Task #1: Task A\nTask #2: Task B` into
`Task #1: Task AXX\nXXTask #2: Task B`, and no AI assertion notices.

Killed by the new `test_kill_55_single_newline_between_tasks` (exact
two-task string) and by the manual suite's
`test_manual_report_two_tasks_joined_with_newline`.

## Why the AI assertions were too weak

All three survivors share one weakness: the AI tests assert properties
("is a string", "contains a title") instead of the function's exact output
contract. The manual suite asserts full equality against a known string, so
every character change is detected. Coverage cannot expose this difference:
both suites execute the same lines, but only the manual suite checks what
those lines produced.
