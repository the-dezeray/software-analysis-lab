# Lab 8 - Visual regression report

## Tool and command

Python Playwright captures the screenshots and Pillow computes the pixel diff.

```powershell
python "lab 8/visual_regression.py" baseline
# deliberate CSS change applied to lab 8/web/index.html
python "lab 8/visual_regression.py" compare
```

## Deliberate UI change

In `lab 8/web/index.html`:

```css
h1 { font-size: 2.6rem; }
#task-list li { padding: .8rem .6rem; }
```

The heading is larger and each task row is taller.

## Result

| Item | Value |
|------|-------|
| Viewport | 1280 x 900 |
| Changed pixels | 37,854 |
| Total pixels | 1,152,000 |
| Pixel difference | **3.286%** |
| Changed region | x=320..960, y=43..376 |

The diff is visible on the heading and the two task rows. The rest of the page
is unchanged.

## Artifacts

- `reports/visual/baseline.png` - before the CSS change
- `reports/visual/current.png` - after the CSS change
- `reports/visual/diff.png` - raw pixel difference
- `reports/visual/highlight.png` - changed pixels highlighted in red
- `reports/visual/report.html` - side-by-side HTML report
- `reports/visual/report.json` - machine-readable percentage and bounding box

## Note

The baseline/current pair is the deliberate CSS-change run. The accessibility
fixes were applied after this comparison, so running `compare` again now will
show a larger diff that includes the new labels and `<main>` wrapper.
