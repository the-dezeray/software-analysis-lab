"""Capture a baseline or compare the current Lab 8 UI against it."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

from web_utils import prepare_page, serve

ROOT = Path(__file__).parent
OUT = ROOT / "reports" / "visual"
BASELINE = OUT / "baseline.png"
CURRENT = OUT / "current.png"
DIFF = OUT / "diff.png"
HIGHLIGHT = OUT / "highlight.png"
REPORT = OUT / "report.html"
SUMMARY = OUT / "report.json"


def capture(page, url: str, path: Path) -> None:
    prepare_page(page, url)
    page.screenshot(path=str(path), full_page=False)


def compare() -> dict:
    baseline = Image.open(BASELINE).convert("RGB")
    current = Image.open(CURRENT).convert("RGB")
    if baseline.size != current.size:
        raise SystemExit(f"Size mismatch: {baseline.size} vs {current.size}")

    diff = ImageChops.difference(baseline, current)
    red, green, blue = diff.split()
    mask = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    mask = mask.point(lambda value: 255 if value else 0)
    changed = sum(count for value, count in enumerate(mask.histogram()) if value)
    total = baseline.width * baseline.height

    diff.save(DIFF)
    highlight = Image.composite(Image.new("RGB", baseline.size, (255, 0, 0)), baseline, mask)
    highlight.save(HIGHLIGHT)

    result = {
        "baseline": str(BASELINE.relative_to(ROOT)),
        "current": str(CURRENT.relative_to(ROOT)),
        "diff": str(DIFF.relative_to(ROOT)),
        "highlight": str(HIGHLIGHT.relative_to(ROOT)),
        "width": baseline.width,
        "height": baseline.height,
        "changed_pixels": changed,
        "total_pixels": total,
        "percent": round(changed / total * 100, 3),
        "changed_bbox": diff.getbbox(),
    }
    SUMMARY.write_text(json.dumps(result, indent=2), encoding="utf-8")
    REPORT.write_text(render_report(result), encoding="utf-8")
    return result


def render_report(result: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Lab 8 visual regression report</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }}
  figure {{ margin: 0; }}
  img {{ width: 100%; border: 1px solid #ccc; }}
  figcaption {{ font-weight: 600; margin-bottom: .3rem; }}
  .score {{ font-size: 1.3rem; }}
</style>
</head>
<body>
<h1>Lab 8 visual regression report</h1>
<p class="score">Pixel difference: <strong>{result["percent"]}%</strong>
({result["changed_pixels"]} of {result["total_pixels"]} pixels)</p>
<p>Changed region: {result["changed_bbox"]}</p>
<div class="grid">
  <figure><figcaption>Baseline</figcaption><img src="baseline.png" alt="Baseline screenshot" /></figure>
  <figure><figcaption>Current</figcaption><img src="current.png" alt="Current screenshot" /></figure>
  <figure><figcaption>Difference (red)</figcaption><img src="highlight.png" alt="Highlighted difference" /></figure>
</div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["baseline", "compare"])
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    with serve() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
        page = context.new_page()
        try:
            if args.mode == "baseline":
                capture(page, base_url, BASELINE)
                print(f"Baseline saved to {BASELINE}")
            else:
                if not BASELINE.exists():
                    raise SystemExit("Run the baseline command first.")
                capture(page, base_url, CURRENT)
                result = compare()
                print(f"Visual difference: {result['percent']}% ({result['changed_pixels']} pixels)")
                print(f"Report: {REPORT}")
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    main()
