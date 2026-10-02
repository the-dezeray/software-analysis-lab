# Lab 4 - Requirements Document (supplied requirements, reconstructed from repo)

Source: reverse-engineered from `app/tasks.py`, `app/cli.py`, and `tests/test_tasks.py`.
No separate spec file exists in the repo, so these 7 functional requirements
were agreed as the baseline for this lab.

| Req ID | Requirement Description |
|--------|-------------------------|
| FR-01 | The system shall allow adding a new task with a title (default priority 1, no tags, not done). |
| FR-02 | The system shall allow marking a task as done by its ID, returning True on success and False if the ID does not exist. |
| FR-03 | The system shall return all pending (not-done) tasks, including every task in the list. |
| FR-04 | The system shall return the average priority across all tasks, and return 0 when the task list is empty. |
| FR-05 | The system shall find and return the first task matching a given title, or None if not found. |
| FR-06 | The system shall remove a task by its ID. |
| FR-07 | The system shall apply a 20% loyalty discount (price * 0.8) for premium users and charge full price otherwise. Price must be 0-10000, flag must be bool; anything else is rejected (see Lab 3 spec). |
