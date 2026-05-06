#!/usr/bin/env python3
"""
sitemap.xml'e 10 yeni blog yazısını ekler.
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "public" / "sitemap.xml"
TODAY = date.today().isoformat()

new_blogs = [
    "blog-e-devlet-deprem-riski-sorgulama",
    "blog-kentsel-donusum-vergisi-muafiyeti",
    "blog-bina-deprem-performans-raporu-nedir",
    "blog-kolon-kesme-cezasi-ve-hukuki-sorumluluk",
    "blog-deprem-sigortasi-prim-hesaplama",
    "blog-deprem-aninda-balkon-guvenli-mi",
    "blog-deprem-sonrasi-gida-saklama-ve-su-temini",
    "blog-eski-bina-deprem-yonetmeligi-uyum",
    "blog-deprem-sonrasi-psikolojik-ilk-yardim",
    "blog-komsu-binasi-deprem-riski-sikayet",
]

text = SITEMAP.read_text(encoding="utf-8")

# Build entries for new blogs
new_entries = ""
for slug in new_blogs:
    url = f"https://yakinimdakideprem.com/{slug}.html"
    if url in text:
        continue   # skip if already present
    new_entries += f"""
  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""

# Also bump blog.html lastmod
text = re.sub(
    r"(<loc>https://yakinimdakideprem\.com/blog\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)",
    rf"\g<1>{TODAY}\g<2>",
    text,
)

# Insert new entries before </urlset>
if new_entries:
    text = text.replace("</urlset>", new_entries + "\n\n</urlset>")

SITEMAP.write_text(text, encoding="utf-8")
print(f"Sitemap updated: {len(new_blogs)} new entries (or skipped if already present), blog.html lastmod={TODAY}")
