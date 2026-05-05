#!/usr/bin/env python3
"""
Şehir görsellerini sayfalara entegre eder:
1. <head> içinde og:image / twitter:image meta tag'larını şehre özel görsele çevirir
2. Statik passage bloğunun başına <figure> ekler (Wikipedia attribution ile)

Marker: <!-- SSR-IMAGE-START --> ... <!-- SSR-IMAGE-END --> (passage içinde)

Kullanım:
  python3 scripts/integrate_city_images.py            # tüm şehirler
  python3 scripts/integrate_city_images.py --slug istanbul
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ALIASES = ROOT / "scripts" / "city_aliases.json"
CREDITS = ROOT / "scripts" / "city_image_credits.json"
CITIES_DIR = PUBLIC / "images" / "cities"

IMG_START = "<!-- SSR-IMAGE-START -->"
IMG_END = "<!-- SSR-IMAGE-END -->"


def build_figure(slug: str, name: str, credit: dict) -> str:
    wiki_url = credit.get("wikipedia_url", "")
    title = credit.get("title", name)
    return (
        f"{IMG_START}\n"
        f'            <figure class="city-hero">\n'
        f'                <img src="/images/cities/{slug}.webp" '
        f'alt="{name} şehrinden manzara — sismik aktivite haritası ile birlikte" '
        f'loading="eager" width="800" height="450">\n'
        f'                <figcaption>'
        f'{name} şehir görseli — '
        f'<a href="{wiki_url}" target="_blank" rel="noopener noreferrer">'
        f'Wikipedia: {title}</a> (CC-BY-SA / kamu malı)'
        f'</figcaption>\n'
        f'            </figure>\n'
        f"            {IMG_END}"
    )


def integrate(slug: str, name: str, credits: dict) -> str:
    page = PUBLIC / f"deprem-{slug}.html"
    img = CITIES_DIR / f"{slug}.webp"
    og = CITIES_DIR / f"{slug}-og.webp"
    credit = credits.get(slug, {})

    if not page.exists():
        return "missing-page"
    if not img.exists() or not credit:
        return "no-image"

    html = page.read_text(encoding="utf-8")

    # ----- 1. og:image / twitter:image güncelle -----
    og_url = f"https://yakinimdakideprem.com/images/cities/{slug}-og.webp"
    html = re.sub(
        r'(<meta\s+property="og:image"\s+content=)"[^"]+"',
        rf'\1"{og_url}"',
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta\s+name="twitter:image"\s+content=)"[^"]+"',
        rf'\1"{og_url}"',
        html,
        count=1,
    )

    # ----- 2. <figure> bloğu — passage'ın hemen sonrasına ekle -----
    figure = build_figure(slug, name, credit)

    if IMG_START in html:
        html = re.sub(
            re.escape(IMG_START) + r".*?" + re.escape(IMG_END),
            figure,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # Passage'ın <h2>...</h2> sonrasına, ilk <p>'den önce ekle
        new_html, n = re.subn(
            r'(<section class="about-city-quakes"[^>]*>\s*\n\s*<h2>[^<]+</h2>)\s*\n',
            r'\1\n            ' + figure + '\n',
            html,
            count=1,
        )
        if n == 0:
            return "no-passage-anchor"
        html = new_html

    page.write_text(html, encoding="utf-8")
    return "integrated"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug")
    args = p.parse_args()

    cities = json.loads(ALIASES.read_text(encoding="utf-8"))
    credits = json.loads(CREDITS.read_text(encoding="utf-8")) \
              if CREDITS.exists() else {}

    targets = {args.slug: cities[args.slug]} if args.slug else cities
    counts = {}
    for slug, info in targets.items():
        result = integrate(slug, info["name"], credits)
        counts[result] = counts.get(result, 0) + 1
    print("Result:", counts)


if __name__ == "__main__":
    main()
