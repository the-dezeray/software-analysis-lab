# Lab 9 - Exploratory testing charter

| Field | Value |
|-------|-------|
| Charter ID | CH-09-01 |
| Feature | Task lifecycle and JSON persistence |
| Mission | Explore the task lifecycle (add -> pending -> complete -> remove -> re-add -> save/reload) for data-integrity, state-transition, ID-generation, and persistence/error-handling failures |
| Time-box | 45 minutes, single session, hard stop |
| Date | 25/10/2026 |
| Build | commit `bc1bb28`, working tree dirty (Labs 7-8 uncommitted) |
| Environment | Windows, Python 3.14.6, pytest 9.1.1 |
| Code under test | `app/tasks.py`, `app/storage.py` (`load_tasks` / `save_tasks` / `format_task_report`), `app/cli.py` |
| Session notes | `session-notes.md` |
| Report | `session-report.md` |

## Mission statement

> Within a 45-minute time-box, explore the task lifecycle - add, list pending,
> complete, remove, re-add, and save/reload - through the Python API and the
> CLI, to expose data-integrity, state-transition, ID-generation, and
> persistence/error-handling failures.

## Why this feature

The task lifecycle is the centre of the application:

- `id` is the handle used by both `complete_task` and `remove_task`, so any
  ID-generation fault becomes a wrong-task fault.
- `get_pending_tasks` is the only listing the CLI prints, so a filtering fault
  is immediately user-visible.
- `tasks.json` is the only durable state. If it is written non-atomically or
  read without validation, the whole task list can be lost.
- Earlier labs tested these functions in isolation (Labs 1, 3, 4, 6, 7), but
  none ran a lifecycle/persistence session across them. That gap is the target.

## Scope

### In scope

| Area | Functions / artefacts |
|------|-----------------------|
| Create | `add_task` (title, default priority, tags, generated id) |
| Read | `get_pending_tasks`, `format_task_report`, CLI output |
| Update | `complete_task` (by id, repeat completion, missing id) |
| Delete | `remove_task` (first/middle/last, missing id, empty list) |
| Persistence | `save_tasks` / `load_tasks`, missing file, round-trip, corrupt or wrong-shaped JSON, encoding |
| Interface | CLI exit codes, `Loaded N tasks`, `Pending tasks: N` |

### Out of scope

- `calculate_discount` (Lab 3), `days_until_due` (date arithmetic),
  `build_query` (SQL construction) - separate features with their own lab
  coverage.
- The Lab 5 / Lab 8 web UI, visual regression, and accessibility.
- Security review beyond what the lifecycle exposes (hardcoded API key is
  already logged in Lab 4).
- Performance, concurrency, and multi-user behaviour.

## Requirements used as oracles

Taken from `lab 4/requirements.md`; P-01/P-02/R-01 are derived oracles because
the written requirements do not cover persistence or the CLI.

| ID | Requirement / oracle | Source |
|----|----------------------|--------|
| FR-01 | Add a task with a title; default priority 1, no tags, not done. | Lab 4 |
| FR-02 | Complete a task by id; return `True` on success, `False` if absent. | Lab 4 |
| FR-03 | Return **all** pending tasks, including every task in the list. | Lab 4 |
| FR-06 | Remove a task by id. | Lab 4 |
| P-01 | A saved list reloads with the same ids, titles, priorities, tags, and done flags. | Derived (docstrings, round-trip) |
| P-02 | A missing or corrupt task file must not crash the app or silently fabricate tasks. | Derived (`load_tasks` docstring) |
| R-01 | CLI counts and report must agree with the API state. | Derived (`cli.py` intent) |

## Heuristics and risk map (SFDIPOT)

| Letter | Focus for this charter | Why it is risky here | Probe family |
|--------|------------------------|----------------------|--------------|
| **S**tructure | Shape of a task dict; required keys; defaults | Hand-edited or legacy JSON may omit `id`/`title`; code indexes keys directly | Load partial/foreign shapes, report them |
| **F**unction | CRUD transitions, idempotency, missing ids | `complete` returns a bool but `remove` does not; repeat calls may silently do nothing | Repeat each operation; call with absent id |
| **D**ata | IDs after delete, titles, priorities, tags, empty lists | `id = len(tasks) + 1` is sensitive to deletion and to loaded gaps | Delete then add; load gapped ids; boundary inputs |
| **I**nterfaces | JSON file, CLI stdout, Python return values | The file is the only durable interface; CLI trusts the API blindly | Round-trip, corrupt file, compare CLI vs API |
| **P**latform | Windows text encoding, file system, BOM | Windows editors/PowerShell commonly write UTF-8 with BOM; `load_tasks` asks for plain `utf-8` | Write BOM-prefixed JSON and run the CLI |
| **O**perations | Save/load, partial writes, report generation | `open(..., "w")` truncates before serialization succeeds | Force a serialization failure and reload |
| **T**ime | Ordering, repeated sessions, stale file | A stale or half-written file can outlive the process that wrote it | Re-run the CLI against leftover files |

Additional heuristics: CRUD lifecycle, boundary values, invalid input,
round-trip consistency, and "what does the user actually see?".

## Session rules

1. Hard stop at `T+45:00`; no probes after the stop marker.
2. Log every observation, bug, question, and new idea live in
   `session-notes.md`; do not wait until the end.
3. Do not fix code, tests, or data. This is a discovery session only.
4. Run persistence probes in a temporary directory outside the repo so
   `tasks.json` never leaks into the working tree.
5. Tag every logged bug at the end by severity and by source:
   `AI-01`..`AI-05` for an AI-suggested avenue, `SELF` for an own probe or
   heuristic.
6. A bug counts as AI-sourced only if the first probe that exposed it came
   from that AI avenue; overlaps are noted but never double-counted.

## Exit criteria

- Charter scope either covered or explicitly recorded as not reached.
- Every reported defect has a minimal inline reproduction and an observed
  actual result.
- Every defect has a severity and a source tag.
- Session report states the AI-vs-manual split by count and by severity weight.

## Deliverables

| Lab requirement | Output |
|-----------------|--------|
| Test charter | this file |
| Pre-session AI ideas | `ai-ideas.md` |
| Timestamped session notes | `session-notes.md` |
| Session report with bug list, severity, AI-vs-manual split | `session-report.md` |
