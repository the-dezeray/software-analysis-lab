# Lab 6 - Step 1: assistant selection

Selected assistant: Muse Spark (the AI assistant used for this session - free tier).
Responding check (02/10/2026): asked "reply with the word READY" - it replied READY.
So the tool counts as configured and responding.

Target functions (all three currently have zero tests - verified with
`grep` over `tests/`, no matches):
1. `find_task_by_title` in `app/tasks.py` (line 65)
2. `remove_task` in `app/tasks.py` (line 73)
3. `format_task_report` in `app/storage.py` (line 8)
