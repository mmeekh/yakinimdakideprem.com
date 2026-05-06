#!/usr/bin/env python3
"""
Tüm sayfa-görsel ilişkilerini image sitemap'e ekler:
- 58 blog sayfası (her biri kendi hero görseli)
- 81 şehir sayfası (her biri kendi şehir görseli)
- Anasayfa (og görseli)
- Blog index (og görseli)

Google Image Search'de tüm görsellerin görünmesi için.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
IMAGES = PUBLIC / "images"
OUT = PUBLIC / "sitemap-images.xml"
ALIASES = ROOT / "scripts" / "city_aliases.json"

entries = []


def add_entry(page_url: str, image_url: str, title: str, caption: str = ""):
    entries.append(f"""  <url>
    <loc>{page_url}</loc>
    <image:image>
      <image:loc>{image_url}</image:loc>
      <image:title>{title}</image:title>
      <image:caption>{caption or title}</image:caption>
      <image:license>https://yakinimdakideprem.com/kullanim-sartlari.html</image:license>
    </image:image>
  </url>""")


def get_meta(html_path: Path) -> tuple[str, str, str]:
    """HTML'den title, description, og:image çıkar."""
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    title_m = re.search(r"<title>([^<]+)</title>", html)
    desc_m = re.search(r'<meta name="description"\s+content="([^"]+)"', html)
    img_m = re.search(r'<meta property="og:image"\s+content="([^"]+)"', html)
    title = title_m.group(1).strip() if title_m else ""
    desc = desc_m.group(1).strip() if desc_m else ""
    img = img_m.group(1).strip() if img_m else ""
    return title, desc, img


# ----- 1. Anasayfa + blog index -----
for slug, page in [("/", "index.html"), ("/blog.html", "blog.html"),
                    ("/son-dakika-deprem.html", "son-dakika-deprem.html"),
                    ("/deprem-aninda.html", "deprem-aninda.html"),
                    ("/ilk-yardim-cantasi.html", "ilk-yardim-cantasi.html"),
                    ("/ben-kimim.html", "ben-kimim.html"),
                    ("/turkiye-deprem-rehberi-fay-hatlari.html", "turkiye-deprem-rehberi-fay-hatlari.html")]:
    f = PUBLIC / page
    if not f.exists():
        continue
    title, desc, img = get_meta(f)
    if img:
        add_entry(f"https://yakinimdakideprem.com{slug}", img, title, desc)

# ----- 2. 58 blog sayfası -----
for blog in sorted(PUBLIC.glob("blog-*.html")):
    title, desc, img = get_meta(blog)
    if img:
        page_url = f"https://yakinimdakideprem.com/{blog.name}"
        add_entry(page_url, img, title, desc)

# ----- 3. 81 şehir sayfası -----
cities = json.loads(ALIASES.read_text(encoding="utf-8"))
for slug, info in cities.items():
    page = PUBLIC / f"deprem-{slug}.html"
    if not page.exists():
        continue
    title, desc, _ = get_meta(page)
    page_url = f"https://yakinimdakideprem.com/deprem-{slug}.html"
    # Şehir hero (Wikipedia'dan çekilen)
    hero = IMAGES / "cities" / f"{slug}.webp"
    if hero.exists():
        add_entry(
            page_url,
            f"https://yakinimdakideprem.com/images/cities/{slug}.webp",
            f"{info['name']} şehri",
            f"{info['name']} ili görüntüsü ve deprem aktivitesi",
        )
    # Şehir OG görseli
    og = IMAGES / "cities" / f"{slug}-og.webp"
    if og.exists():
        add_entry(
            page_url,
            f"https://yakinimdakideprem.com/images/cities/{slug}-og.webp",
            f"{info['name']} deprem haritası",
            f"{info['name']} ili anlık deprem ve risk haritası",
        )

# ----- Generate XML -----
xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{chr(10).join(entries)}
</urlset>
"""

OUT.write_text(xml, encoding="utf-8")
print(f"sitemap-images.xml: {len(entries)} image entries written")
