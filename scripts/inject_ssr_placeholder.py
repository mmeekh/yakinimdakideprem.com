#!/usr/bin/env python3
"""
Inject SSR freshness placeholder block into all city HTML pages.
Idempotent — running twice is safe.

The block sits right after the city's <h1> and is updated by
city_freshness.py worker when an earthquake occurs in that city.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ALIASES = ROOT / "scripts" / "city_aliases.json"

SSR_START = "<!-- SSR-FRESHNESS-START -->"
SSR_END = "<!-- SSR-FRESHNESS-END -->"

PLACEHOLDER = (
    f"{SSR_START}\n"
    '            <div class="ssr-freshness" aria-live="polite"></div>\n'
    f"            {SSR_END}"
)

cities = json.loads(ALIASES.read_text(encoding="utf-8"))
done, skipped, missing = 0, 0, 0

for slug in cities:
    page = PUBLIC / f"deprem-{slug}.html"
    if not page.exists():
        missing += 1
        continue

    html = page.read_text(encoding="utf-8")
    if SSR_START in html:
        skipped += 1
        continue

    # Inject after first <h1>...</h1>
    new_html, n = re.subn(
        r"(<h1[^>]*>[^<]+</h1>)",
        r"\1\n            " + PLACEHOLDER,
        html,
        count=1,
    )
    if n == 0:
        print(f"SKIP {slug} — no <h1> found")
        skipped += 1
        continue

    page.write_text(new_html, encoding="utf-8")
    done += 1

print(f"Injected: {done}  Skipped: {skipped}  Missing: {missing}")
