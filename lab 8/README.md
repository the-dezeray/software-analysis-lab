# Lab 8 - Visual regression and accessibility testing

A minimal Lab 8 setup built on the existing Lab 5 task-manager UI. The Lab 5
page is copied to `lab 8/web/index.html`; Lab 5 itself is left untouched.

## Tools

- Python Playwright + Pillow for screenshot comparison (no BackstopJS install).
- `axe-core 4.10.2`, vendored at `lab 8/vendor/axe.min.js`.
- A small local `http.server` so the page and `localStorage` behave normally.

## Results

| Check | Result |
|-------|--------|
| Visual baseline vs deliberate CSS change | **3.286%** pixel difference (37,854 pixels) |
| Accessibility before fixes | 4 violations |
| Accessibility after fixes | **0 violations** (33 passes) |

The two WCAG A/AA fixes were missing accessible names for the form controls
and insufficient colour contrast. The two landmark best-practice findings were
also fixed by adding `<main>`.

## Files

- `web/index.html` - Lab 8 UI copy with seeded accessibility issues and fixes.
- `web_utils.py` - local server + deterministic page setup.
- `visual_regression.py` - `baseline` / `compare` screenshot workflow.
- `a11y_scan.py` - axe-core scan, JSON + HTML output.
- `visual-report.md` - visual diff result.
- `accessibility-report.md` - triage table, fixes and before/after result.
- `reflection.md` - pixel diff vs accessibility discussion.
- `reports/visual/` - baseline, current, diff, highlight, HTML report.
- `reports/a11y/` - before/after JSON and HTML reports.
- `vendor/axe.min.js` - axe-core 4.10.2.

## Setup

```powershell
pip install -r "lab 8/requirements.txt"
python -m playwright install chromium
```

## Run

```powershell
# Visual baseline, then apply the deliberate CSS change and compare
python "lab 8/visual_regression.py" baseline
python "lab 8/visual_regression.py" compare

# Accessibility before fixes
python "lab 8/a11y_scan.py" before

# Apply the label/contrast/main fixes, then re-scan
python "lab 8/a11y_scan.py" after
```

The saved visual report is the deliberate CSS-change run. The accessibility
fixes were applied afterwards, so a fresh `compare` now includes those changes
too.

## Deliverable map

| Lab requirement | Output |
|-----------------|--------|
| Visual regression diff report | `reports/visual/report.html`, `highlight.png`, 3.286% in `visual-report.md` |
| Accessibility reports before/after | `reports/a11y/before.*`, `reports/a11y/after.*` |
| Triage table | `accessibility-report.md` |
| Two fixes + confirmation | labels + contrast fixes, after scan shows 0 violations |
| Reflection | `reflection.md` |
