# Lab 9 - Timestamped session notes

| Field | Value |
|-------|-------|
| Charter | `CH-09-01` (see `charter.md`) |
| Date | 25/10/2026 |
| Time-box | 45:00 (hard stop) |
| Session clock | `T+mm:ss` |
| Build | commit `bc1bb28`, dirty working tree |
| Environment | Windows, Python 3.14.6, pytest 9.1.1 |
| Baseline | `pytest -q`: 6 failed, 37 passed in 5.80 s |
| Workspace | `%TEMP%\lab9-*` (outside the repo) |
| Logging rule | Every observation, bug, question, and idea logged live |

> **Time-box disclosure:** `T+mm:ss` is a session-clock position, not a
> wall-clock time. The session was executed as a compressed run of the
> 45-minute box. Every command and result below is real and reproducible; no
> application file, test, or data file in the repository was modified.

## Timestamped log

| Time | Area | Probe / observation | Type | Sev | Source | Evidence |
|------|------|---------------------|------|-----|--------|----------|
| T+00:00 | Baseline | `pytest -q` -> **6 failed, 37 passed**. In-charter failure: `test_get_pending_tasks_includes_first_task`. The other 5 are `average_priority` (out of scope) and 4 discount cases (out of scope). | OBS | - | SELF | `FAILED tests/test_tasks.py::test_get_pending_tasks_includes_first_task` |
| T+00:00 | Baseline | Empty temp dir, `python -m app.cli` -> `Loaded 0 tasks`, blank report line, `Pending tasks: 0`, exit 0. | OBS | - | SELF | exit 0 |
| T+00:02 | Setup | Created `%TEMP%\lab9-session` and `%TEMP%\lab9-cli2`; `PYTHONPATH` pointed at the repo. All persistence probes run from the temp dir so the repo's `tasks.json` is never touched. | OBS | - | SELF | `tasks.json` absent in repo before and after |
| T+00:04 | ID | Starting AI-01: ids are the handle for both complete and remove, so check uniqueness before trusting any later result. | IDEA | - | AI-01 | - |
| T+00:06 | ID | Add A, B, C; remove id 2; add D -> `[(1,'A'), (3,'C'), (3,'D')]`. D reuses C's id. | **BUG B1** | Major | AI-01 | `add_task` id formula |
| T+00:08 | ID | Add A, B; remove id 1; add C -> `[(2,'B'), (2,'C')]`. Reproduced on the first-item path. | **BUG B1** | Major | AI-01 | repeat |
| T+00:09 | ID | Add A; remove id 1; add B -> id 1 again, but only one task remains, so no duplicate. Confirms the formula is `len(tasks) + 1`, not `max(id) + 1`. | OBS | - | AI-01 | `[(1,'B')]` |
| T+00:10 | ID | Save ids `[1,3]`, reload, add -> new task gets id 3, colliding with the loaded task. The fault also enters through persisted data. | **BUG B1** | Major | AI-01 | duplicate id after reload |
| T+00:11 | State | Starting AI-02: walk the pending list at 0, 1, and 3 tasks. | IDEA | - | AI-02 | - |
| T+00:13 | State | `get_pending_tasks([])` -> `[]`; one pending task -> **`[]`**; three pending tasks -> **`['B','C']`**. The first item is always skipped. | **BUG B2** | Major | AI-02 | `range(1, len(tasks))` |
| T+00:15 | State | Two tasks, complete the first, list pending -> `['B']`. Looks correct, but the first task was already done, so the skip is masked. A single happy-path check would miss B2. | OBS | - | AI-02 | masking effect |
| T+00:17 | State | `complete_task` id 1 twice -> `(True, True)`; missing id 99 -> `False`. Idempotent and FR-02-consistent. | OBS | - | AI-02 | - |
| T+00:18 | State | `complete_task(t, "1")` -> `False`; `complete_task(t, True)` -> `True` on task id 1; `remove_task` returns `None` for both success and missing id. Logged as an open question, not a defect (no return contract for remove). | Q | - | SELF | bool/int equality |
| T+00:20 | Input | Starting AI-03: blank, whitespace, `None`, very long, and non-string titles. | IDEA | - | AI-03 | - |
| T+00:22 | Input | `add_task` accepted `""`, `"   "`, `"\t\n"`, and `None`; each produced a task with FR-01's "title" field empty or non-string. The web UI rejects blank titles, so core and UI disagree. | **BUG B3** | Moderate | AI-03 | all accepted |
| T+00:24 | Input | `add_task(t, None)` then `format_task_report(t)` -> `TypeError: can only concatenate str (not "NoneType") to str`. An accepted task later crashes the only report. | **BUG B3** | Moderate | AI-03 | traceback captured |
| T+00:25 | Input | A 5,000-character title was accepted and stored. No length requirement exists, so recorded as a question, not a defect. | Q | - | AI-03 | length 5000 |
| T+00:26 | Input | `tags=["work"]`; add task; append `"mutated"` to the caller's list -> stored task now reports `['work','mutated']`. `tags="work"` is also accepted and stored as a string. | **BUG B4** | Minor | AI-03 | aliasing |
| T+00:27 | Input | Priorities `0`, `4`, `-5`, `"2"`, `None` all accepted. A string priority later raises `TypeError` in `average_priority`. `average_priority` is out of charter, but the invalid state is created in scope by `add_task`. | **BUG B5** | Minor | AI-03 | `total += "2"` |
| T+00:29 | Persist | Starting AI-04: missing file, valid round-trip, then deliberately corrupt files. | IDEA | - | AI-04 | - |
| T+00:30 | Persist | No file -> `[]`. Valid save/reload preserved ids, titles, priorities, tags, and `done` exactly. Happy path is sound. | OBS | - | AI-04 | round-trip equal |
| T+00:31 | Persist | `tasks.json` = `{not json` -> `JSONDecodeError`; empty file -> `JSONDecodeError`. CLI exits 1 with a raw traceback. | **BUG B6** | Major | AI-04 | traceback |
| T+00:33 | Persist | Valid JSON with the wrong shape: `null` -> `load_tasks()` returns `None`, CLI crashes at `len(tasks)`; `{"a":1}` -> CLI prints **`Loaded 1 tasks`** then crashes in the report; `[1,2]` -> report raises `TypeError: 'int' object is not subscriptable`. | **BUG B6** | Major | AI-04 | 3 shapes |
| T+00:35 | Persist | Own extension of AI-04: what if `save_tasks` fails *after* the file is opened for writing? The write mode truncates first. | IDEA | - | SELF | code read: `open(..., "w")` |
| T+00:37 | Persist | Saved a valid task, then set `task["tags"] = {"x"}` and saved. `TypeError: Object of type set is not JSON serializable`; file on disk is now `[{"id": 1, ..., "tags": ` (truncated), and `load_tasks()` raises `JSONDecodeError`. The entire task file is lost. | **BUG B7** | Major | SELF | before/after file contents |
| T+00:39 | Platform | Own platform heuristic: Windows PowerShell 5.1 `Set-Content -Encoding utf8` and Notepad's "UTF-8 with BOM" both prepend a BOM. Try a BOM-prefixed file. | IDEA | - | SELF | Windows default |
| T+00:40 | Platform | A valid JSON file with a UTF-8 BOM -> `JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig)`; CLI exits 1. This actually happened while seeding the first CLI fixtures, before it was reproduced deliberately. | **BUG B8** | Moderate | SELF | BOM bytes `EF BB BF` |
| T+00:42 | CLI | Starting AI-05. Seeded BOM-free files (after B8): 3 pending -> `Pending tasks: 2`; 1 pending -> `0`; 2 pending -> `1`; first done + second pending -> `1`. The mismatch reproduces B2's user-visible symptom; AI-05 introduced no new root cause. | OBS | Major | AI-05 | stdout captured |
| T+00:43 | CLI | The done-first case is correct by coincidence: the skipped first task is already done. Confirms that CLI-only checks can hide B2 and that the root cause belongs to AI-02, not a separate CLI bug. | OBS | - | AI-05 | 2 tasks, first done |
| T+00:44 | CLI | Report prints only `Task #n: title`; a completed task looks identical to a pending one, and priority/tags are absent. No written requirement defines the report format, so logged as an open question. | Q | - | AI-05 | `format_task_report` |
| **T+00:45** | **STOP** | **Time-box reached. No further probes.** | **STOP** | - | - | - |

## Post-box triage (outside the 45-minute box)

No new testing was performed in this section. The eight provisional findings
were de-duplicated, given final ids, and severity-checked against the
definitions below.

**Severity scale used:** Critical = data loss/security on a normal path;
Major = core requirement wrong or crash with a workaround; Moderate = edge/
validation failure or crash with corrupted input; Minor = usability or API
consistency issue.

| Raw | Final | Title | Severity | Source | Why this severity |
|-----|-------|-------|----------|--------|-------------------|
| B2 | **BUG-01** | `get_pending_tasks` skips the first task | Major | AI-02 | FR-03 is wrong on every list where the first task is pending; workaround exists (iterate manually), but the CLI reports the wrong count. |
| B1 | **BUG-02** | Id reuse after deletion creates duplicate ids | Major | AI-01 | Ids are the handle for complete/remove; duplicates make those operations hit the wrong task. Requires a delete-then-add sequence, so not Critical. |
| B7 | **BUG-03** | `save_tasks` truncates before serializing; failure loses the file | Major | SELF | Total file loss is Critical impact, but the trigger is a non-JSON-serializable field, so likelihood keeps it at Major. |
| B6 | **BUG-04** | `load_tasks` trusts any JSON shape; corrupt files crash the CLI | Major | AI-04 | The app is unusable until the file is manually repaired or deleted; no safe fallback exists. |
| B3 | **BUG-05** | `add_task` accepts blank/non-string titles; `None` later crashes the report | Moderate | AI-03 | Boundary validation gap; collapse requires a non-string title, but that title is accepted without complaint. |
| B8 | **BUG-06** | UTF-8 BOM files are rejected | Moderate | SELF | Common on Windows; blocks startup, but the fix (re-save without BOM) is easy. |
| B4 | **BUG-07** | `tags` stored by reference; string tags accepted | Minor | AI-03 | Silent shared-state mutation, but no crash and no data loss until a later save. |
| B5 | **BUG-08** | Priority values and types are not validated | Minor | AI-03 | Invalid state is accepted; downstream `average_priority` crash is outside this charter. No explicit P1-P3 range in the written requirements. |

## Questions and unconfirmed risks

1. **Report contract.** `format_task_report` prints only id and title. Done
   state, priority, and tags are invisible, so a completed task is
   indistinguishable from a pending one. No requirement specifies the format,
   so this is a specification gap rather than a confirmed defect.
2. **Title length.** A 5,000-character title is accepted. No length limit is
   written down; the web UI's input has no `maxlength` either.
3. **CLI functionality.** `app/cli.py` only loads and prints; it exposes no
   add/complete/remove command. The lifecycle exists only in the Python API.
   This is a product-scope question, not a defect against the current module.
4. **Id types.** `complete_task(t, "1")` silently returns `False`, while
   `complete_task(t, True)` succeeds on id 1 because `True == 1`. Python
   semantics, but surprising for a public API. Not counted as a defect.
5. **Concurrency and file permissions.** Not tested: simultaneous writers,
   read-only `tasks.json`, and disk-full during `save_tasks`. The non-atomic
   write in BUG-03 makes these likely to be destructive, but they are
   unconfirmed.
6. **Unicode.** Not tested: the shell pipe mangled non-ASCII input during
   setup, so no claim is made about Unicode titles or encoding round-trips.
