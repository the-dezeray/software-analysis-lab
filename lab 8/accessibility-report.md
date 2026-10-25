# Lab 8 - Accessibility report

## Tool and command

The scan injects the vendored `axe-core 4.10.2` into the page and runs
`axe.run()` through Playwright.

```powershell
python "lab 8/a11y_scan.py" before
python "lab 8/a11y_scan.py" after
```

The Lab 8 copy deliberately removes the field labels and adds low-contrast
helper text so the scan produces WCAG A/AA findings. The original Lab 5 page
only had the two landmark best-practice findings.

## Triage table - before fixes

| Rule | WCAG | Impact | Nodes | Finding | Fix applied |
|------|------|--------|-------|---------|-------------|
| `select-name` | 2.1 A (4.1.2) | critical | 1 | Priority select has no accessible name | Added `<label for="priority-input">Priority</label>` |
| `color-contrast` | 2.1 AA (1.4.3) | serious | 2 | `.muted` text is `#aaa` on white (2.32:1); completed task text is `#888` (3.54:1) | Changed both to `#555` |
| `landmark-one-main` | best practice | moderate | 1 | Page has no `<main>` landmark | Wrapped page content in `<main>` |
| `region` | best practice | moderate | 7 | Content is not contained in a landmark | Same `<main>` wrapper |

The input also received an explicit `<label for="task-input">Task title</label>`
for consistency, even though axe did not flag it separately in this run.

## Fixes applied

1. Added visible labels for both form controls.
2. Raised text contrast: `.muted` from `#aaa` to `#555`, and completed-task
   text from `#888` to `#555`.
3. Wrapped the page content in `<main>` to clear the two landmark findings.

## Result after fixes

| Metric | Before | After |
|--------|--------|-------|
| Violations | 4 | **0** |
| Passes | - | 33 |
| Incomplete | - | 0 |

All four findings are resolved. The two WCAG A/AA findings (`select-name` and
`color-contrast`) are confirmed fixed, and the two landmark best-practice
findings are fixed as well.

## Artifacts

- `reports/a11y/before.json` - full axe result before fixes
- `reports/a11y/before.html` - readable before report
- `reports/a11y/after.json` - full axe result after fixes
- `reports/a11y/after.html` - readable after report
