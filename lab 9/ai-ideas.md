# Lab 9 - Pre-session AI co-pilot ideas

These five ideas were generated **before** the timer started, using the charter
in `charter.md`. They are avenues to explore, not test scripts and not bug
predictions. The session then mixed them with own instincts and heuristics.

## Prompt used (verbatim)

> You are my exploratory-testing co-pilot. I have a 45-minute charter:
> "Explore the task lifecycle - add, list pending, complete, remove, re-add,
> and save/reload - through the Python API and the CLI, to expose
> data-integrity, state-transition, ID-generation, and persistence/error-
> handling failures." In scope: add_task, get_pending_tasks, complete_task,
> remove_task, load_tasks/save_tasks, format_task_report, app/cli.py. Out of
> scope: calculate_discount, days_until_due, build_query, web UI.
>
> Using SFDIPOT, propose five distinct exploratory testing ideas specific to
> this scope. For each, name it, give the SFDIPOT letter, explain why it is
> high-risk here, and list 2-3 concrete probes with expected vs suspicious
> outcomes. Do not write tests or fixes.

## Source-attribution rule

A defect is tagged **AI-nn** when the first probe that exposed it came from
that AI-suggested avenue. It is tagged **SELF** when it came from an own
instinct, a deviation, or an extension made during the session. If an AI
avenue and an own instinct overlap, the defect is counted once, under the
avenue that produced the first failing observation, and the overlap is noted
in the report.

## Summary

| ID | SFDIPOT | Idea | Probes | Unique defects |
|----|---------|------|--------|----------------|
| AI-01 | Data | ID generation after deletion | 4 | 1 (`BUG-02`) |
| AI-02 | Function | CRUD state transitions: empty / one / many | 6 | 1 (`BUG-01`) |
| AI-03 | Data | Title, priority, and tag validation | 8 | 3 (`BUG-05`, `BUG-07`, `BUG-08`) |
| AI-04 | Interface | Persistence corruption and reload | 5 | 1 (`BUG-04`) |
| AI-05 | Operations | CLI report and counts vs actual state | 5 | 0 new root causes |

---

## AI-01 - ID generation after deletion

- **SFDIPOT:** Data.
- **Why high-risk:** `add_task` derives the id from `len(tasks) + 1`, not from
  the largest existing id. Deleting a task shrinks the list, so the next add
  can reuse an id that is still in use. `complete_task` and `remove_task` both
  match on id, so a duplicate id means the wrong task is acted on.
- **Probes:**
  1. Add A, B, C; remove B; add D; inspect every `(id, title)`.
     *Expected:* all ids unique. *Suspicious:* a repeated id.
  2. Add A, B; remove A; add C; inspect ids.
     *Expected:* new task gets a fresh id. *Suspicious:* C reuses B's id.
  3. Add A; remove A; add B.
     *Expected:* ids unique. *Suspicious:* id 1 reused (acceptable only if no
     other task holds it).
  4. Save a list with ids `[1, 3]`, reload, add a task.
     *Expected:* id 4. *Suspicious:* id 3, colliding with the loaded task.
- **Outcome:** probe 1 returned `[(1,'A'), (3,'C'), (3,'D')]`; probe 2 returned
  `[(2,'B'), (2,'C')]`. Logged as `BUG-02`. Probe 4 reproduced the same root
  cause from persisted data.

## AI-02 - CRUD state transitions: empty / one / many

- **SFDIPOT:** Function.
- **Why high-risk:** Off-by-one faults and missing-state handling usually only
  appear at the boundaries. The starter test already hints at a pending-task
  problem, but one test is not a lifecycle.
- **Probes:**
  1. `get_pending_tasks([])`.
     *Expected:* `[]`. *Suspicious:* a crash.
  2. One pending task.
     *Expected:* that task. *Suspicious:* `[]`.
  3. Three pending tasks.
     *Expected:* all three. *Suspicious:* fewer than three, or a missing first
     item.
  4. Two tasks, complete the first, then list pending.
     *Expected:* the second task only. *Suspicious:* a count that only looks
     right because the first task was already done.
  5. Complete the same id twice; complete a missing id.
     *Expected:* idempotent success then `False`. *Suspicious:* a crash or a
     wrong boolean.
  6. Remove first, middle, last, and missing ids.
     *Expected:* only the requested task disappears. *Suspicious:* an
     exception or a shifted task.
- **Outcome:** probe 2 returned `[]`, probe 3 returned `['B','C']`. Logged as
  `BUG-01`. Probe 4 showed that completing the first task masks the fault:
  the pending list looks correct while the first task is still skipped.
  Probes 5-6 were consistent with FR-02/FR-06, apart from an id-type edge
  recorded as an observation.

## AI-03 - Title, priority, and tag validation

- **SFDIPOT:** Data.
- **Why high-risk:** The canonical task dict is built inside `add_task` with no
  validation. Bad values do not fail at the boundary; they fail later in
  `format_task_report`, `average_priority`, or JSON serialization, far from the
  cause. The web UI trims and rejects empty titles, so the core and the UI
  disagree about what a valid task is.
- **Probes:**
  1. Titles: `""`, `"   "`, `"\t\n"`, `None`, a 5,000-character string.
     *Expected:* blank/non-string rejected. *Suspicious:* accepted.
  2. Feed an accepted bad title into `format_task_report`.
     *Expected:* no crash. *Suspicious:* `TypeError`.
  3. Priorities: `0`, `4`, `-5`, `"2"`, `None`.
     *Expected:* reject outside the UI's P1-P3 range and reject non-integers.
     *Suspicious:* accepted; later arithmetic fails.
  4. Tags: pass a list, then mutate it after `add_task`; pass a string.
     *Expected:* task keeps its own copy and a list. *Suspicious:* the stored
     task changes, or a string is stored.
- **Outcome:** all title probes were accepted; `None` later crashed the report.
  Logged as `BUG-05`. Tag aliasing and string tags were confirmed as
  `BUG-07`. Invalid priorities were accepted and a string priority broke
  `average_priority`; logged as `BUG-08`.

## AI-04 - Persistence corruption and reload

- **SFDIPOT:** Interface.
- **Why high-risk:** `load_tasks` calls `json.load` and returns the result
  directly. JSON is syntactically valid for `null`, `{}`, and `[1, 2]`, but
  none of those is a task list. A corrupt file is also the most likely
  aftermath of an interrupted write.
- **Probes:**
  1. No file present.
     *Expected:* `[]`. *Suspicious:* a crash.
  2. Save a valid list, reload, compare every field.
     *Expected:* exact round-trip. *Suspicious:* lost `tags`, `done`, or type
     changes.
  3. Truncated or malformed JSON (`{not json`, empty file).
     *Expected:* a clear error or a safe fallback. *Suspicious:* a raw
     traceback.
  4. Valid JSON of the wrong shape: `null`, `{}`, `{"a":1}`, `[1,2]`.
     *Expected:* rejected as "not a task list". *Suspicious:* returned as if
     it were tasks.
  5. Run the CLI against each corrupt file.
     *Expected:* a non-zero exit with a useful message. *Suspicious:* a
     traceback, or a misleading `Loaded N tasks`.
- **Outcome:** the happy-path round-trip passed. Every corrupt shape failed:
  malformed/empty raised `JSONDecodeError`, `null` crashed `len()`, `{"a":1}`
  printed `Loaded 1 tasks` then crashed, and `[1,2]` crashed the report.
  Logged as `BUG-04`.

## AI-05 - CLI report and counts vs actual state

- **SFDIPOT:** Operations.
- **Why high-risk:** The CLI is the only user-facing entry point. It prints
  `Loaded N`, the report, and `Pending tasks: N` without cross-checking them.
  A wrong API result is therefore presented as fact.
- **Probes:**
  1. Seed three pending tasks, run the CLI, compare the printed count with the
     three report rows.
  2. Seed one pending task; compare `Pending tasks:` with the one row.
  3. Seed two pending tasks; compare.
  4. Seed two tasks with the first done; compare.
  5. Inspect whether the report distinguishes done from pending, or shows
     priority/tags.
- **Outcome:** printed counts were 2, 0, and 1 against 3, 1, and 2 actual
  pending tasks. This is the user-visible symptom of `BUG-01`, not a new root
  cause, so it is credited to AI-02. The done-first case printed the correct
  count by coincidence, which shows why a single CLI check is not enough.
  The report showed only `Task #n: title`; done state, priority, and tags are
  invisible. Recorded as an open question, not a defect, because no written
  requirement specifies the report format.

## Overlap noted before the timer

AI-05 (CLI counts) is largely a second view of AI-02 (pending state). AI-03
(validation) overlaps the instinctive "try empty and invalid input" heuristic.
The report therefore separates **raw attribution** (which avenue produced the
first failing observation) from **unique AI contribution** (which defects the
AI avenue introduced that an own instinct would probably not have reached).
