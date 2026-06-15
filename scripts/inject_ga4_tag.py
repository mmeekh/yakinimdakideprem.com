#!/usr/bin/env python3
"""
GA4 gtag.js etiketini gtag taşımayan TÜM sayfalara enjekte eder.

Sorun: GTM container'ında (GTM-WQZS53QX) hiç GA4 etiketi yok; 142 sayfa sadece
GTM yüklüyor → GA4'e (G-J03Y3ZWDWD) SIFIR veri gidiyor. Yalnız 20 sayfada
hardcoded gtag var. Bu script kalan ~154 sayfaya aynı gtag snippet'ini ekler.

GTM'de GA4 tag OLMADIĞI için çift sayım riski YOK. İdempotent: G-J03Y3ZWDWD
zaten varsa sayfa atlanır.

Kullanım:
  python3 scripts/inject_ga4_tag.py            # tüm public/*.html
  python3 scripts/inject_ga4_tag.py --dry-run  # sadece raporla
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
GA4_ID = "G-J03Y3ZWDWD"

SNIPPET = (
    "<!-- Google tag (gtag.js) — GA4 -->\n"
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>\n'
    "<script>\n"
    "  window.dataLayer = window.dataLayer || [];\n"
    "  function gtag(){dataLayer.push(arguments);}\n"
    "  gtag('js', new Date());\n"
    f"  gtag('config', '{GA4_ID}');\n"
    "</script>\n"
)


def process(path: Path, dry: bool) -> str:
    html = path.read_text(encoding="utf-8")
    if GA4_ID in html:
        return "skip"          # zaten gtag var (20 sayfa)
    if "</head>" not in html:
        return "no-head"
    if dry:
        return "would-inject"
    new_html = html.replace("</head>", SNIPPET + "</head>", 1)
    path.write_text(new_html, encoding="utf-8")
    return "injected"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    counts: dict[str, int] = {}
    for f in sorted(PUBLIC.glob("*.html")):
        r = process(f, args.dry_run)
        counts[r] = counts.get(r, 0) + 1
    print("Result:", counts)


if __name__ == "__main__":
    main()
