Linger Caught errors 
- **Defect #1 (`tags=[]`)** — mutable default argument: ruff `B006` / pylint `W0102`.
- **Defect #7 (`== True`)** — flake8 `E712`.
- **Defect #8 (unclosed `open`)** — with-open rules (ruff `SIM115` / pylint `consider-using-with`).
- **Defect #5 (implicit `None` return)** — pylint `inconsistent-return-statements`.
- **Defect #10 (hardcoded `API_KEY`)** — security scanners (bandit / gitleaks), not a syntax linter.



NOT CAUGHT BY THE LINTER
- **Defect #3 (off-by-one `range(1, ...)`)** — loop logic is syntactically legal; only a spec review of `get_pending_tasks`'s docstring ("all tasks that are not yet done") reveals the skipped index 0.
- **Defect #4 (empty-list division)** — the code divides by `len(tasks)` with no guard; a linter sees a normal expression, only reasoning about the empty case exposes the crash.
- **Defect #9 (string + integer)** — plain linters do not type-check data values; needs a static type checker (e.g., mypy/pyright) or a runtime read.
- **Defect #2 (ID collisions)** — requires tracing the add → remove → add lifecycle, not visible in any single line.
- **Defect #11 (SQL injection)** — syntactically valid SQL string; requires treating user input as untrusted.
- **Defect #12 (date truncation)** — requires knowing `datetime.now()` carries a time component; depends on runtime values.
