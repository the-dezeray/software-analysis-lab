"""Run an axe-core accessibility scan against the Lab 8 page."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

from web_utils import prepare_page, serve

ROOT = Path(__file__).parent
AXE = ROOT / "vendor" / "axe.min.js"
OUT = ROOT / "reports" / "a11y"


def render_report(result: dict, label: str) -> str:
    violations = result.get("violations", [])
    rows = []
    for violation in violations:
        tags = ", ".join(violation.get("tags", []))
        nodes = "<br>".join(
            html.escape(json.dumps(node.get("target", [])))
            for node in violation.get("nodes", [])
        )
        rows.append(
            "<tr>"
            f"<td>{html.escape(violation.get('id', ''))}</td>"
            f"<td>{html.escape(tags)}</td>"
            f"<td>{html.escape(str(violation.get('impact', '')))}</td>"
            f"<td>{len(violation.get('nodes', []))}</td>"
            f"<td>{html.escape(violation.get('help', ''))}</td>"
            f"<td>{nodes}</td>"
            "</tr>"
        )
    table = "".join(rows) or "<tr><td colspan='6'>No violations found.</td></tr>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Lab 8 accessibility report - {html.escape(label)}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ccc; padding: .5rem; text-align: left; vertical-align: top; }}
  th {{ background: #f3f3f3; }}
</style>
</head>
<body>
<h1>Lab 8 accessibility report - {html.escape(label)}</h1>
<p>Violations: <strong>{len(violations)}</strong> |
Passes: {len(result.get("passes", []))} |
Incomplete: {len(result.get("incomplete", []))}</p>
<table>
<thead><tr><th>Rule</th><th>WCAG tags</th><th>Impact</th><th>Nodes</th><th>Help</th><th>Targets</th></tr></thead>
<tbody>{table}</tbody>
</table>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("label", choices=["before", "after"])
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    with serve() as base_url, sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        try:
            prepare_page(page, base_url)
            page.add_script_tag(path=str(AXE))
            result = page.evaluate("async () => await axe.run()")
        finally:
            browser.close()

    (OUT / f"{args.label}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (OUT / f"{args.label}.html").write_text(render_report(result, args.label), encoding="utf-8")

    violations = result.get("violations", [])
    print(f"{args.label}: {len(violations)} violations")
    for violation in violations:
        print(f"  {violation['id']} [{violation.get('impact')}] {len(violation['nodes'])} node(s)")


if __name__ == "__main__":
    main()
