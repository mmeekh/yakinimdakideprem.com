#!/usr/bin/env python3
"""
10 yeni blog için kapsamlı SEO optimizasyonu:

1. Görselleri 1536x864'e resize + quality 82 → ~150KB civarı
2. IPTC/XMP metadata enjekte (creator, copyright, description)
3. Blog HTML'lerine eklenecekler:
   - <picture> + srcset + width/height
   - ImageObject schema (license, creditText, creator)
   - Yazar byline (E-E-A-T sinyali)
   - "Son güncelleme" zaman damgası
   - Okuma süresi tahmini
   - Görünür breadcrumb (mobile-friendly)
   - article:* OG meta tag'leri
   - Önerilen yazılar bölümü zaten var
4. sitemap-images.xml — image sitemap üret
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
IMAGES = PUBLIC / "images"
BLOG_CFG = ROOT / "scripts" / "blog_configs_2026_05.json"

TODAY = date.today().isoformat()
PUBLISH_DATE = "2026-05-05"

# ---------- 1. Görselleri optimize et ----------
def optimize_image(path: Path, target_w=1536, target_h=864, quality=82):
    """Resize + quality reduce. Korur aspect ratio."""
    img = Image.open(path).convert("RGB")
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    dst_ratio = target_w / target_h

    # Cover-fit (görselin tamamını kullan, orta crop)
    if src_ratio > dst_ratio:
        new_w = int(src_h * dst_ratio)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    else:
        new_h = int(src_w / dst_ratio)
        offset = (src_h - new_h) // 2
        img = img.crop((0, offset, src_w, offset + new_h))

    img = img.resize((target_w, target_h), Image.LANCZOS)
    img.save(path, "WEBP", quality=quality, method=6)


# ---------- 2. IPTC/XMP metadata via exiftool ----------
def inject_metadata(path: Path, title: str, description: str):
    """Exiftool ile IPTC + XMP metadata yaz. Yoksa skip."""
    try:
        subprocess.run([
            "exiftool", "-overwrite_original",
            "-XMP-dc:Creator=Emin Kılıç",
            "-XMP-dc:Rights=© 2026 Yakınımdaki Deprem - Emin Kılıç",
            f"-XMP-dc:Title={title}",
            f"-XMP-dc:Description={description}",
            "-IPTC:By-line=Emin Kılıç",
            "-IPTC:CopyrightNotice=© 2026 Yakınımdaki Deprem",
            f"-IPTC:Caption-Abstract={description}",
            f"-IPTC:Headline={title}",
            "-IPTC:Source=https://yakinimdakideprem.com",
            str(path),
        ], capture_output=True, check=False, timeout=30)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass   # exiftool yoksa sessizce skip


# ---------- 3. Reading time ----------
def estimate_reading_minutes(cfg: dict) -> int:
    """Konfigden tahmini kelime sayısı → dakika."""
    word_count = len(cfg["lead"].split())
    for h2, paragraphs in cfg["body_h2_blocks"]:
        word_count += len(h2.split())
        for p in paragraphs:
            word_count += len(re.sub(r"<[^>]+>", "", p).split())
    for q, a in cfg["faqs"]:
        word_count += len(q.split()) + len(a.split())
    # 250 kelime/dakika (Türkçe)
    return max(3, round(word_count / 250))


# ---------- 4. Update blog HTML ----------
def upgrade_blog_html(slug: str, cfg: dict):
    page = PUBLIC / f"blog-{slug}.html"
    if not page.exists():
        print(f"SKIP {slug}: HTML yok")
        return

    html = page.read_text(encoding="utf-8")
    title = cfg["title"]
    desc = cfg["meta_description"]
    img_url = f"https://yakinimdakideprem.com/images/blog-{slug}.webp"
    canonical = f"https://yakinimdakideprem.com/blog-{slug}.html"
    reading_min = estimate_reading_minutes(cfg)
    primary_keyword = cfg["keywords"][0]

    # Better alt: primary keyword + descriptive
    img_alt = f"{cfg['image_alt']} — {primary_keyword} rehberi"

    # ----- a) Update <img> alt + add width/height + decoding async -----
    old_img = re.compile(
        r'<div class="blog-hero" style="background-image: url\(\'images/blog-'
        + re.escape(slug) + r"\.webp'\);\">"
    )
    if old_img.search(html):
        # Replace background-image div with proper <picture> for SEO
        new_hero = (
            f'<div class="blog-hero">\n'
            f'                <picture>\n'
            f'                    <img src="images/blog-{slug}.webp" '
            f'alt="{img_alt}" width="1536" height="864" '
            f'fetchpriority="high" decoding="async">\n'
            f'                </picture>\n'
            f'                <div class="overlay"></div>'
        )
        html = old_img.sub(new_hero, html)
        # Remove the old <div class="overlay"></div> that follows
        html = re.sub(
            r'(' + re.escape(new_hero) + r')\s*\n\s*<div class="overlay"></div>',
            r'\1', html, count=1
        )

    # ----- b) article:* OG meta tags ekle (eğer yoksa) -----
    article_og = (
        f'    <meta property="article:published_time" content="{PUBLISH_DATE}T00:00:00+03:00">\n'
        f'    <meta property="article:modified_time" content="{TODAY}T00:00:00+03:00">\n'
        f'    <meta property="article:author" content="https://yakinimdakideprem.com/ben-kimim.html">\n'
        f'    <meta property="article:section" content="Deprem Güvenliği">\n'
    )
    for kw in cfg["keywords"][:5]:
        article_og += f'    <meta property="article:tag" content="{kw}">\n'

    if "article:published_time" not in html:
        html = html.replace(
            '<meta property="og:type" content="article">',
            '<meta property="og:type" content="article">\n' + article_og.rstrip(),
            1,
        )

    # ----- c) Reading time + last updated + author byline (visible) -----
    # Mevcut .meta div'ini bul ve genişlet
    meta_replacement = (
        f'<div class="meta">\n'
        f'                        <span><i class="far fa-calendar" aria-hidden="true"></i> '
        f'<time datetime="{PUBLISH_DATE}" itemprop="datePublished">5 Mayıs 2026</time></span>\n'
        f'                        <span><i class="far fa-clock" aria-hidden="true"></i> '
        f'Son güncelleme: <time datetime="{TODAY}" itemprop="dateModified">{TODAY}</time></span>\n'
        f'                        <span><i class="far fa-user" aria-hidden="true"></i> '
        f'<a href="/ben-kimim.html" itemprop="author"><strong>Emin Kılıç</strong></a></span>\n'
        f'                        <span><i class="fas fa-book-reader" aria-hidden="true"></i> '
        f'{reading_min} dk okuma</span>\n'
        f'                    </div>'
    )
    html = re.sub(
        r'<div class="meta">[\s\S]*?</div>',
        meta_replacement, html, count=1,
    )

    # ----- d) Breadcrumb (görünür) - h1'den önce -----
    breadcrumb_html = (
        f'<nav class="breadcrumb" aria-label="İçerik konumu" itemscope '
        f'itemtype="https://schema.org/BreadcrumbList">\n'
        f'                <a href="/" itemscope itemtype="https://schema.org/ListItem" '
        f'itemprop="itemListElement"><span itemprop="name">Ana Sayfa</span>'
        f'<meta itemprop="position" content="1"></a>\n'
        f'                <span aria-hidden="true">›</span>\n'
        f'                <a href="/blog.html" itemscope itemtype="https://schema.org/ListItem" '
        f'itemprop="itemListElement"><span itemprop="name">Blog</span>'
        f'<meta itemprop="position" content="2"></a>\n'
        f'                <span aria-hidden="true">›</span>\n'
        f'                <span itemscope itemtype="https://schema.org/ListItem" '
        f'itemprop="itemListElement"><span itemprop="name">{title}</span>'
        f'<meta itemprop="position" content="3"></span>\n'
        f'            </nav>'
    )
    if 'class="breadcrumb"' not in html:
        # Hero içindeki h1'den ÖNCE ekle
        html = re.sub(
            r'(<div class="hero-content">)\s*\n\s*(<h1>)',
            r'\1\n                ' + breadcrumb_html + r'\n                \2',
            html, count=1,
        )

    # ----- e) Yazar bio kutusu (sayfa altına) -----
    author_box = """
                <aside class="author-box" itemscope itemtype="https://schema.org/Person">
                    <div class="author-box__avatar">
                        <img src="/icons/logo.png" alt="Yakınımdaki Deprem logosu" width="80" height="80" loading="lazy">
                    </div>
                    <div class="author-box__info">
                        <p class="author-box__label">Yazar</p>
                        <h3 itemprop="name">Emin Kılıç</h3>
                        <p itemprop="description">Yakınımdaki Deprem'in kurucusu ve geliştiricisi. AFAD ve Kandilli Rasathanesi verilerini canlı işleyen bağımsız bir afet bilgilendirme platformu yürütüyor. Deprem güvenliği, yapı yönetmeliği ve afet hazırlığı konularında 100'den fazla rehber yayımladı.</p>
                        <p class="author-box__links">
                            <a href="/ben-kimim.html" itemprop="url"><i class="fas fa-user-circle"></i> Yazar Sayfası</a>
                            <a href="https://www.linkedin.com/in/emin-k%C4%B1l%C4%B1%C3%A7-250b14210/" target="_blank" rel="noopener noreferrer me" itemprop="sameAs"><i class="fab fa-linkedin"></i> LinkedIn</a>
                        </p>
                    </div>
                </aside>"""
    # H2 "Sıkça Sorulan Sorular"'dan ÖNCE
    if 'class="author-box"' not in html:
        html = re.sub(
            r'(<h2>Sıkça Sorulan Sorular</h2>)',
            author_box + r'\n\n                \1',
            html, count=1,
        )

    page.write_text(html, encoding="utf-8")


# ---------- 5. Image sitemap (sitemap-images.xml) ----------
def generate_image_sitemap(blogs: list[dict]):
    sm = PUBLIC / "sitemap-images.xml"
    entries = []
    for cfg in blogs:
        slug = cfg["slug"]
        loc = f"https://yakinimdakideprem.com/blog-{slug}.html"
        img_url = f"https://yakinimdakideprem.com/images/blog-{slug}.webp"
        entries.append(f"""  <url>
    <loc>{loc}</loc>
    <image:image>
      <image:loc>{img_url}</image:loc>
      <image:title>{cfg['title']}</image:title>
      <image:caption>{cfg['image_alt']}</image:caption>
      <image:license>https://yakinimdakideprem.com/kullanim-sartlari.html</image:license>
    </image:image>
  </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{chr(10).join(entries)}
</urlset>
"""
    sm.write_text(xml, encoding="utf-8")
    print(f"Image sitemap: {sm.name}")


# ---------- Main ----------
def main():
    blogs = json.loads(BLOG_CFG.read_text(encoding="utf-8"))
    for cfg in blogs:
        slug = cfg["slug"]
        img_path = IMAGES / f"blog-{slug}.webp"
        if img_path.exists():
            print(f"Optimizing {slug} ...", end=" ")
            optimize_image(img_path)
            inject_metadata(img_path, cfg["title"], cfg["meta_description"])
            print(f"{img_path.stat().st_size // 1024} KB")
        upgrade_blog_html(slug, cfg)
    generate_image_sitemap(blogs)
    print(f"\nDone. {len(blogs)} blogs optimized.")


if __name__ == "__main__":
    main()
