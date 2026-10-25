# Lab 9 - Session report

## 1. Summary

A single 45-minute exploratory session was run against the task lifecycle and
JSON persistence of the sample task manager. Eight defects were logged: four
Major, two Moderate, and two Minor. No Critical defect was confirmed.

- **Raw source split:** 6 of 8 defects (75.0%) were first exposed by an
  AI-suggested avenue; 2 of 8 (25.0%) came from own heuristics.
- **Severity-weighted split:** 72.2% AI-suggested, 27.8% self-found.
- **Adjusted unique AI contribution:** 2 of 8 defects (25.0%) would probably
  not have been probed without the AI list. The difference between 75% and
  25% is the main finding of the session and is discussed in section 9.

The highest-value finds were duplicate ids after a delete-then-add sequence
(`BUG-02`) and valid-but-wrong-shaped JSON being accepted as a task list
(`BUG-04`). Both came from AI avenues. The two persistence finds that the AI
list missed, a truncating save (`BUG-03`) and UTF-8 BOM rejection (`BUG-06`),
came from own reliability and platform instincts.

## 2. Charter recap

> Within a 45-minute time-box, explore the task lifecycle - add, list pending,
> complete, remove, re-add, and save/reload - through the Python API and the
> CLI, to expose data-integrity, state-transition, ID-generation, and
> persistence/error-handling failures.

| In scope | Out of scope |
|----------|--------------|
| `add_task`, `get_pending_tasks`, `complete_task`, `remove_task` | `calculate_discount`, `days_until_due`, `build_query` |
| `load_tasks`, `save_tasks`, `format_task_report` | Lab 5 / Lab 8 web UI, visual and accessibility testing |
| `app/cli.py` output and exit codes | Performance, concurrency, multi-user behaviour |

Full charter: `charter.md`. Pre-session AI ideas and prompt: `ai-ideas.md`.
Live log: `session-notes.md`.

## 3. Session facts

| Field | Value |
|-------|-------|
| Charter ID | CH-09-01 |
| Date | 25/10/2026 |
| Time-box | 45:00, hard stop at `T+45:00` |
| Build | commit `bc1bb28`, dirty working tree |
| Environment | Windows, Python 3.14.6, pytest 9.1.1 |
| Baseline suite | 6 failed, 37 passed in 5.80 s |
| Probe families | 5 AI avenues plus 2 self-initiated persistence/encoding probes |
| Confirmed defects | 8 (4 Major, 2 Moderate, 2 Minor) |
| Code changes | None - discovery only |

## 4. Coverage

| Area | Scenarios exercised | Outcome |
|------|---------------------|---------|
| Create (`add_task`) | Normal add, defaults, 3 sequential adds, empty/whitespace/`None`/5,000-char titles, priorities 0/4/-5/`"2"`/`None`, list and string tags, caller mutation after add | `BUG-02`, `BUG-05`, `BUG-07`, `BUG-08` |
| Read (`get_pending_tasks`) | Empty, one, three, done-first, after reload | `BUG-01` |
| Complete (`complete_task`) | Valid id, repeat, missing id, string id, bool id | Consistent with FR-02 apart from an id-type edge recorded as a question |
| Remove (`remove_task`) | First, middle, last, missing id, empty list | List state correct; no success/failure signal (question, not counted) |
| Persistence (`save_tasks` / `load_tasks`) | Missing file, valid round-trip, malformed JSON, empty file, `null`, `{}`, `{"a":1}`, `[1,2]`, UTF-8 BOM, serialization failure during save | `BUG-03`, `BUG-04`, `BUG-06` |
| Report / CLI | Empty list, 1/2/3 pending, done-first, corrupt files, exit codes | `BUG-01` symptom; report-format question |

**Not reached or not tested:** simultaneous writers, read-only file, disk-full,
Unicode round-trip, very large files, duplicate-title lookup, concurrency, and
all out-of-scope modules. The time-box stopped the session before these.

**Coverage judgement:** the lifecycle's happy path is sound (add, complete,
remove, and a clean save/reload all behave as specified). The defects cluster
at boundaries: the first element of a list, deletion followed by creation,
non-list JSON, and non-happy-path file writes.

## 5. Defect list

| ID | Defect | Severity | Source | Requirement |
|----|--------|----------|--------|-------------|
| BUG-01 | `get_pending_tasks` skips the first task | Major | AI-02 | FR-03 |
| BUG-02 | Id reuse after deletion creates duplicate ids | Major | AI-01 | FR-01 / FR-02 / FR-06 |
| BUG-03 | `save_tasks` truncates the file before serializing; a failure loses all tasks | Major | SELF | P-01 |
| BUG-04 | `load_tasks` trusts any JSON shape; corrupt or foreign files crash the CLI | Major | AI-04 | P-02 / R-01 |
| BUG-05 | `add_task` accepts blank/non-string titles; `None` later crashes the report | Moderate | AI-03 | FR-01 |
| BUG-06 | Valid JSON with a UTF-8 BOM is rejected | Moderate | SELF | P-02 |
| BUG-07 | `tags` are stored by reference; string tags are accepted | Minor | AI-03 | FR-01 |
| BUG-08 | Priority values and types are not validated | Minor | AI-03 | FR-01 (inferred) |

Severity scale: **Critical** = data loss/security on a normal path; **Major** =
core requirement wrong or crash with a workaround; **Moderate** = edge or
validation failure, or crash on corrupted input; **Minor** = usability or API
consistency.

### BUG-01 - `get_pending_tasks` skips the first task (Major, AI-02)

- **Where:** `app/tasks.py:50`, `for i in range(1, len(tasks))`.
- **Expected (FR-03):** every not-done task, including index 0.
- **Actual:** index 0 is never examined. One pending task returns `[]`; three
  pending tasks return only the second and third.
- **Repro:**

```python
from app.tasks import add_task, get_pending_tasks
tasks = []
add_task(tasks, "A")
add_task(tasks, "B")
print([t["title"] for t in get_pending_tasks(tasks)])
# actual: ['B']   expected: ['A', 'B']
```

- **User-visible evidence:** a `tasks.json` with three pending tasks makes the
  CLI print `Pending tasks: 2`.
- **Impact:** the core listing is wrong whenever the first task is pending.
  When the first task is done, the output accidentally looks correct, which is
  why one happy-path check is not enough.
- **Source note:** the starter test already hinted at this, but the AI-02
  empty/one/many walk produced the first minimal failing probe (`one pending
  -> []`). Counted as AI-02 under the attribution rule.

### BUG-02 - Id reuse after deletion creates duplicate ids (Major, AI-01)

- **Where:** `app/tasks.py:28`, `"id": len(tasks) + 1`.
- **Expected:** a new task gets an id that no current task holds.
- **Actual:** after any removal, `len + 1` can reuse an id that is still in
  the list.
- **Repro:**

```python
from app.tasks import add_task, complete_task, remove_task
tasks = []
add_task(tasks, "A"); add_task(tasks, "B"); add_task(tasks, "C")
remove_task(tasks, 2)          # remove B
add_task(tasks, "D")           # D gets id 3, same as C
print([(t["id"], t["title"]) for t in tasks])
# [(1, 'A'), (3, 'C'), (3, 'D')]

complete_task(tasks, 3)        # marks only C; D stays pending
print([(t["id"], t["title"], t["done"]) for t in tasks])
# [(1, 'A', False), (3, 'C', True), (3, 'D', False)]
```

- **Impact:** `complete_task` and `remove_task` match the first id, so a
  duplicate id silently targets the wrong task. The report also shows two
  `Task #3` rows, so the user cannot tell them apart.
- **Source note:** the AI-01 avenue explicitly asked for delete-then-add id
  checks. This was the clearest case of the AI list producing a probe an own
  "add a task" instinct would have skipped.

### BUG-03 - `save_tasks` truncates before serializing; failure loses the file (Major, SELF)

- **Where:** `app/tasks.py:19-20`, `open(TASKS_FILE, "w")` followed by
  `json.dump`.
- **Expected:** a failed save leaves the previous file intact, or writes to a
  temporary file and replaces atomically.
- **Actual:** the `"w"` open truncates the only copy. If `json.dump` raises,
  the file is left as a partial JSON fragment.
- **Repro:**

```python
from app.tasks import add_task, load_tasks, save_tasks
tasks = []
add_task(tasks, "A")
save_tasks(tasks)

tasks[0]["tags"] = {"x"}       # any non-JSON value; also models an encoding/disk failure
try:
    save_tasks(tasks)
except TypeError as e:
    print("save failed:", e)

print(open("tasks.json", encoding="utf-8").read())
# actual: [{"id": 1, "title": "A", "priority": 1, "tags": 

load_tasks()                   # JSONDecodeError: Expecting value
```

- **Impact:** every task is lost and the app cannot start until the file is
  repaired or deleted. This is Critical impact but a narrower trigger, so it
  is triaged Major.
- **Source note:** this was an own extension of the AI-04 persistence avenue:
  AI-04 covered corrupt files on read, not partial writes. Counted SELF.

### BUG-04 - `load_tasks` trusts any JSON shape (Major, AI-04)

- **Where:** `app/tasks.py:10-13`, `json.load` result returned directly.
- **Expected (P-02):** a missing or corrupt file must not crash the app or
  fabricate tasks; a non-list should be rejected clearly.
- **Actual:** only malformed JSON raises. Valid JSON of the wrong type is
  returned as if it were a task list.
- **Repro (one file at a time):**

```python
# tasks.json = 'null'
load_tasks()          # returns None
# python -m app.cli  -> TypeError: object of type 'NoneType' has no len()

# tasks.json = '{"a": 1}'
# python -m app.cli  -> "Loaded 1 tasks" then
# TypeError: string indices must be integers, not 'str'

# tasks.json = '[1, 2]'
format_task_report(load_tasks())
# TypeError: 'int' object is not subscriptable

# tasks.json = '{not json'
# python -m app.cli  -> JSONDecodeError, exit 1
```

- **Impact:** any corrupt, hand-edited, or foreign-shaped file makes the CLI
  unusable and, in the object case, prints a misleading `Loaded 1 tasks`
  before crashing. Combined with BUG-03, a failed save produces exactly this
  state.
- **Source note:** AI-04's "valid JSON of the wrong shape" probe was the
  direct cause; malformed JSON alone would have been less revealing.

### BUG-05 - Blank/non-string titles are accepted (Moderate, AI-03)

- **Where:** `app/tasks.py:23-35`, no validation before the task dict is built.
- **Expected (FR-01):** add a task *with a title*; blank and non-string values
  should be rejected at the boundary, as the web UI does (`trim()` and
  `if (!title)`).
- **Actual:** `""`, `"   "`, `"\t\n"`, and `None` are all stored. A `None`
  title later crashes `format_task_report`.
- **Repro:**

```python
from app.tasks import add_task
from app.storage import format_task_report
tasks = []
add_task(tasks, None)
format_task_report(tasks)
# TypeError: can only concatenate str (not "NoneType") to str
```

- **Impact:** invalid tasks enter the store, survive a round-trip, and break
  the only report. The failure is far from the cause.
- **Source note:** prompted by AI-03; the "empty string" case is also a
  standard instinct, so this is a partial overlap.

### BUG-06 - UTF-8 BOM files are rejected (Moderate, SELF)

- **Where:** `app/tasks.py:11`, `encoding="utf-8"`.
- **Expected:** a valid JSON file saved by a Windows tool should load, or the
  app should report a clear, actionable error.
- **Actual:** a BOM-prefixed file raises
  `JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig)` and the
  CLI exits 1.
- **Repro:** write a normal task list with a UTF-8 BOM (for example,
  Windows PowerShell 5.1 `Set-Content -Encoding utf8`, or Notepad's
  "UTF-8 with BOM"), then run `python -m app.cli`.
- **Impact:** common Windows interoperability failure; blocks startup until
  the file is re-saved without a BOM.
- **Source note:** found accidentally while seeding the first CLI fixtures,
  then reproduced deliberately. Not suggested by any AI avenue; counted SELF.

### BUG-07 - Tags are stored by reference; strings accepted (Minor, AI-03)

- **Where:** `app/tasks.py:25-31`.
- **Expected:** the task owns its tag list; tags are a list.
- **Actual:** the caller's list is stored directly, and a string is accepted.
- **Repro:**

```python
tags = ["work"]
tasks = []
add_task(tasks, "A", tags=tags)
tags.append("mutated")
print(tasks[0]["tags"])        # ['work', 'mutated']

add_task(tasks, "B", tags="work")
print(tasks[1]["tags"])        # 'work'
```

- **Impact:** silent shared-state mutation after creation; string tags behave
  like a sequence of characters in any later iteration.

### BUG-08 - Priority values and types are not validated (Minor, AI-03)

- **Where:** `app/tasks.py:23-35`.
- **Expected:** priorities consistent with the UI's P1-P3 range and integer
  type. The written requirements only state the default (1), so the range is
  inferred from the web UI, not a formal requirement.
- **Actual:** `0`, `4`, `-5`, `"2"`, and `None` are accepted. A string
  priority later breaks `average_priority`.
- **Repro:**

```python
from app.tasks import add_task, average_priority
tasks = []
add_task(tasks, "A", priority="2")
average_priority(tasks)
# TypeError: unsupported operand type(s) for +=: 'int' and 'str'
```

- **Impact:** an invalid task state survives persistence and crashes later
  arithmetic. `average_priority` is outside this charter; only the invalid
  state created inside `add_task` is in scope.

## 6. AI vs manual source breakdown

### By count

| Source | Defects | Share |
|--------|---------|-------|
| AI-suggested avenue | BUG-01, BUG-02, BUG-04, BUG-05, BUG-07, BUG-08 | **6 / 8 = 75.0%** |
| Self-found | BUG-03, BUG-06 | **2 / 8 = 25.0%** |

### By severity

| Severity | AI-suggested | Self-found | Total |
|----------|--------------|------------|-------|
| Critical (weight 4) | 0 | 0 | 0 |
| Major (weight 3) | 3 | 1 | 4 |
| Moderate (weight 2) | 1 | 1 | 2 |
| Minor (weight 1) | 2 | 0 | 2 |
| **Weighted total** | **13 / 18 = 72.2%** | **5 / 18 = 27.8%** | 18 |

The weighted split is close to the count split because both self-found
defects are above Minor. The one self-found Major is the most destructive
defect in the session (`BUG-03`).

### Per AI avenue

| Avenue | Probes | Defects | Unique to AI? |
|--------|--------|---------|---------------|
| AI-01 - id generation after deletion | 4 | BUG-02 | **Yes** - an add-only instinct would not delete first |
| AI-02 - empty/one/many state transitions | 6 | BUG-01 | Partly - the starter test hinted at it |
| AI-03 - title/priority/tag validation | 8 | BUG-05, BUG-07, BUG-08 | Partly - standard validation instinct |
| AI-04 - persistence corruption | 5 | BUG-04 | **Yes** - `null`/`{}`/`[1,2]` are valid JSON, so a "corrupt file" instinct alone would miss them |
| AI-05 - CLI vs actual state | 5 | 0 new root causes | No - second view of AI-02 |

**AI hit rate:** 4 of 5 avenues produced at least one defect; 2 of 5 produced a
defect that is genuinely unlikely to have been reached unprompted. AI-05
produced no new root cause: its count mismatch is the user-visible symptom of
BUG-01, and the report-format observation was a question, not a defect.

### Adjusted unique AI contribution

| Measure | AI | Self / overlap | Total |
|---------|----|----------------|-------|
| Raw first-probe attribution | 6 (75.0%) | 2 (25.0%) | 8 |
| Judged unique AI contribution | 2 (25.0%) | 6 (75.0%) | 8 |
| Judged unique AI contribution, weighted | 6 / 18 = 33.3% | 12 / 18 = 66.7% | 18 |

The 6 "self / overlap" cases are BUG-01, BUG-03, BUG-05, BUG-06, BUG-07, and
BUG-08: two were self-found and four overlap standard instincts. The two
unique AI cases are BUG-02 and BUG-04.

"Unique" here means: the defect would probably not have been probed from my
own instincts in this session. BUG-02 and BUG-04 pass that test. BUG-01 was
already visible in the baseline suite; BUG-05/07/08 are standard input
validation; BUG-03/06 are own reliability/platform probes. The gap between the
raw 75% and the adjusted 25% is the honest measure of what the AI list added.

## 7. Questions and unconfirmed risks

1. **Report format is a specification gap.** A completed task looks identical
   to a pending one in the CLI, and priority/tags are invisible. No written
   requirement defines the report, so it was not logged as a defect.
2. **No title length limit.** A 5,000-character title is accepted. No limit is
   specified, and the web input has no `maxlength`, so this is a question.
3. **CLI is read-only.** `app/cli.py` cannot add, complete, or remove; the
   lifecycle exists only in the Python API. A product-scope question.
4. **Id type semantics.** `complete_task(t, "1")` returns `False`, while
   `complete_task(t, True)` succeeds on id 1. Python's `True == 1` behaviour
   makes the API surprising, but no contract covers non-integer ids.
5. **Concurrency, permissions, disk-full.** Not tested. BUG-03 suggests these
   would be destructive, but they remain unconfirmed.
6. **Unicode round-trip.** Not tested; the shell pipe mangled non-ASCII input
   during setup, so no claim is made.

## 8. Reproduction

All probes ran from a temporary directory with the repo on `PYTHONPATH`, so
`tasks.json` was created outside the working tree:

```powershell
$tmp = Join-Path $env:TEMP "lab9-repro"
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
Push-Location $tmp
$env:PYTHONPATH = "C:\path\to\task-manager"
python -m app.cli
Pop-Location
```

The per-defect blocks in section 5 are self-contained. For CLI checks, seed a
BOM-free `tasks.json` in the temp directory, for example:

```json
[{"id":1,"title":"A","priority":1,"tags":[],"done":false},
 {"id":2,"title":"B","priority":1,"tags":[],"done":false},
 {"id":3,"title":"C","priority":1,"tags":[],"done":false}]
```

Then `python -m app.cli` prints `Pending tasks: 2`, exposing BUG-01. To
reproduce BUG-06, save the same JSON with a UTF-8 BOM (PowerShell 5.1
`Set-Content -Encoding utf8` or Notepad "UTF-8 with BOM").

## 9. Reflection

**Did the AI-suggested charter lead to bugs I would not have found unprompted,
or did it duplicate my instincts?**

Both, and the split is the useful result.

The AI list changed *where I looked first*. AI-01 (ids after deletion) was the
clearest win: an instinctive "add a task and check it" pass would not delete a
task and then add another. That sequence exposed duplicate ids (BUG-02), a
Major data-integrity defect that contaminates every later by-id operation.
AI-04 was the second win: I would have tested malformed JSON, but probably not
`null`, `{}`, and `[1,2]`. Those are syntactically valid, so they slip past a
"corrupt file" check and reach production as wrong-shaped data (BUG-04).

The rest largely systematised things I would have tried anyway. The baseline
suite already failed on the pending-task test, so BUG-01 was not an AI
discovery; AI-02 just gave it a minimal one-task reproduction and revealed the
masking effect. AI-03's title/priority/tag probes are standard boundary
instincts, and three of its four findings are Minor or Moderate. AI-05 was
almost a duplicate of AI-02: it found no new root cause, only the CLI symptom
of the same pending bug. That duplication is itself worth recording, because a
longer AI list would probably contain more of it.

The AI list also missed the two findings that came from reliability and
platform instincts: a save that truncates before serializing (BUG-03) and
Windows UTF-8 BOM rejection (BUG-06). Both are about the *environment and
failure mode* of persistence, not the task model. The AI's SFDIPOT suggestions
were strong on Data and Function and weak on Platform and Operations failure
modes. A better prompt would have asked explicitly for interrupted writes,
encoding, permissions, and disk-full scenarios.

So the honest answer is: AI-suggested avenues led me to **2 of 8** defects I
would probably have missed (25%), not the 6 of 8 that the raw attribution
suggests. The raw number overstates the AI because the same avenues overlapped
my own instincts and because the AI also had a second view of the same bug.
The value was breadth and sequencing, not unique insight. Used as a checklist,
the AI list is worth the five minutes; used as a substitute for platform and
reliability heuristics, it leaves the most destructive bug unfound.

## 10. Limitations

- **Compressed time-box.** The session was executed as a compressed run of the
  45-minute box; `T+` markers are session-clock positions, not wall-clock
  times. The stop rule was respected: no probes after `T+45:00`.
- **Same agent generated the ideas and ran the probes.** The source tags
  measure *avenue origin*, not independent human vs AI insight. This is the
  main threat to validity and the reason section 6 reports an adjusted unique
  contribution as well as the raw split.
- **Written evidence only.** Per the chosen deliverable format, reproduction
  is inline; there is no raw console log or probe script in the repo.
- **Not exhaustive.** Eight defects in 45 minutes is a sample, not a complete
  audit. Concurrency, permissions, disk-full, Unicode, and the UI were not
  reached.
- **Some overlap with earlier labs.** The pending-task and title-validation
  flaws are seeded defects already visible in Labs 4/6. The session's new
  contribution is the lifecycle/persistence framing and BUG-02/03/04/06.
- **No fixes applied.** Severities are triage-level judgements, not a
  cost/benefit decision, and no regression tests were added.

## 11. Repository impact

Only these files were added:

- `lab 9/charter.md`
- `lab 9/ai-ideas.md`
- `lab 9/session-notes.md`
- `lab 9/session-report.md`
- one `lab 9/` entry in the root `README.md`

No application code, test, fixture, or existing lab file was modified. All
`tasks.json` probes ran in `%TEMP%` and the temporary directories were removed
after the session.
