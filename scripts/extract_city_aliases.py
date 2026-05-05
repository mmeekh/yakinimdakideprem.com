#!/usr/bin/env python3
"""Parse city-keywords.js → city_aliases.json (idempotent, run once)."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "public" / "js" / "city-keywords.js"
OUT = ROOT / "scripts" / "city_aliases.json"

text = JS.read_text(encoding="utf-8")

# Each city line: { slug: "x", name: "Y", ..., keywords: ["a", "b", ...] }
pattern = re.compile(
    r'\{\s*slug:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*region:\s*"([^"]+)"\s*,'
    r'\s*lat:\s*([\d.]+)\s*,\s*lon:\s*([\d.]+)\s*,\s*keywords:\s*\[([^\]]+)\]'
)

cities = {}
for m in pattern.finditer(text):
    slug, name, region, lat, lon, kw_str = m.groups()
    keywords = [k.strip().strip('"') for k in kw_str.split(",")]
    cities[slug] = {
        "name": name,
        "region": region,
        "lat": float(lat),
        "lon": float(lon),
        "aliases": keywords,
    }

OUT.write_text(json.dumps(cities, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Extracted {len(cities)} cities → {OUT}")
