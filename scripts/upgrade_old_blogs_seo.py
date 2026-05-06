#!/usr/bin/env python3
"""
Generic SEO upgrade for ALL blog HTML files.
- Görsel >200KB ise optimize et (1536x864, q82 WebP)
- Breadcrumb yoksa ekle
- Author box yoksa ekle
- article:* OG tags yoksa ekle
- <img>'ye width/height/decoding/fetchpriority ekle
- alt text'e primary keyword bağlamı ekle
- blog-detail.css cache versiyonunu bumple
- "Son güncelleme" zaman damgasını günceller
"""
from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
IMAGES = PUBLIC / "images"

TODAY = date.today().isoformat()
NEW_BLOGS = {
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
}


def optimize_image(path: Path, target_w=1536, target_h=864, quality=82, max_kb=200):
    """Resize sadece >max_kb veya >2000px ise."""
    size_kb = path.stat().st_size // 1024
    img = Image.open(path)
    src_w, src_h = img.size
    if size_kb < max_kb and src_w <= 1600:
        return False, size_kb

    img = img.convert("RGB")
    src_ratio = src_w / src_h
    dst_ratio = target_w / target_h
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
    return True, path.stat().st_size // 1024


def inject_metadata(path: Path, title: str, description: str):
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
        ], capture_output=True, check=False, timeout=20)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass


# ----- Title + image extraction from HTML -----
def parse_html_meta(html: str) -> dict:
    meta = {}
    m = re.search(r"<title>([^<]+)</title>", html)
    meta["title"] = m.group(1).strip() if m else ""
    m = re.search(r'<meta name="description"\s+content="([^"]+)"', html)
    meta["desc"] = m.group(1).strip() if m else ""
    m = re.search(r'<meta name="keywords"\s+content="([^"]+)"', html)
    meta["keywords"] = m.group(1).strip() if m else ""
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", html)
    meta["h1"] = m.group(1).strip() if m else meta["title"]
    # Find primary image (og:image)
    m = re.search(r'<meta property="og:image"\s+content="https://yakinimdakideprem\.com/images/([^"]+)"', html)
    meta["img_filename"] = m.group(1).strip() if m else ""
    return meta


# ----- Build the HTML upgrades -----
def upgrade_html(slug: str, html: str, meta: dict) -> str:
    title = meta["h1"] or meta["title"]
    primary_kw = (meta["keywords"].split(",")[0] if meta["keywords"] else "deprem rehberi").strip()

    # --- a) article:* OG tags ---
    if "article:published_time" not in html and 'property="og:type" content="article"' in html:
        keywords = [k.strip() for k in meta["keywords"].split(",") if k.strip()][:5]
        article_og = (
            f'    <meta property="article:published_time" content="2026-04-20T00:00:00+03:00">\n'
            f'    <meta property="article:modified_time" content="{TODAY}T00:00:00+03:00">\n'
            f'    <meta property="article:author" content="https://yakinimdakideprem.com/ben-kimim.html">\n'
            f'    <meta property="article:section" content="Deprem Güvenliği">\n'
        )
        for kw in keywords:
            article_og += f'    <meta property="article:tag" content="{kw}">\n'

        html = html.replace(
            '<meta property="og:type" content="article">',
            '<meta property="og:type" content="article">\n' + article_og.rstrip(),
            1,
        )

    # --- b) <img> attributes (width/height/decoding/fetchpriority) ---
    # Hero image olarak background-image kullanan blog'larda dönüştür
    if meta["img_filename"]:
        bg_pattern = re.compile(
            r'<div class="blog-hero" style="background-image: url\(\'images/'
            + re.escape(meta["img_filename"])
            + r"'\);\">"
        )
        if bg_pattern.search(html):
            new_hero = (
                f'<div class="blog-hero">\n'
                f'                <picture>\n'
                f'                    <img src="images/{meta["img_filename"]}" '
                f'alt="{title} — {primary_kw} rehberi" '
                f'width="1536" height="864" fetchpriority="high" decoding="async">\n'
                f'                </picture>\n'
                f'                <div class="overlay"></div>'
            )
            html = bg_pattern.sub(new_hero, html)
            # Remove duplicate overlay
            html = re.sub(
                r'<div class="overlay"></div>\s*\n\s*<div class="overlay"></div>',
                '<div class="overlay"></div>',
                html,
                count=1,
            )

    # --- c) Breadcrumb ---
    if 'class="breadcrumb"' not in html:
        breadcrumb = (
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
        html = re.sub(
            r'(<div class="hero-content">)\s*\n\s*(<h1>)',
            r'\1\n                ' + breadcrumb + r'\n                \2',
            html, count=1,
        )

    # --- d) Author box ---
    if 'class="author-box"' not in html:
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
        # H2 "İlgili Rehberler"den ÖNCE veya </article>'tan ÖNCE
        if "<h2>İlgili Rehberler</h2>" in html:
            html = html.replace(
                "<h2>İlgili Rehberler</h2>",
                author_box.lstrip() + "\n\n                <h2>İlgili Rehberler</h2>",
                1,
            )
        elif "</article>" in html:
            html = html.replace(
                "</article>",
                author_box + "\n            </article>",
                1,
            )

    # --- e) Cache version bump ---
    html = re.sub(
        r'blog-detail\.css\?v=\d+',
        'blog-detail.css?v=202605061900',
        html,
    )

    return html


def main():
    blog_files = sorted(PUBLIC.glob("blog-*.html"))
    skipped_new = 0
    upgraded_html = 0
    optimized_imgs = 0
    total_kb_saved = 0

    for f in blog_files:
        slug = f.stem
        if slug in NEW_BLOGS:
            skipped_new += 1
            continue   # zaten optimize edildi

        html = f.read_text(encoding="utf-8")
        meta = parse_html_meta(html)

        # Optimize image if exists
        if meta["img_filename"]:
            img_path = IMAGES / meta["img_filename"]
            if img_path.exists():
                old_size = img_path.stat().st_size // 1024
                changed, new_size = optimize_image(img_path)
                if changed:
                    inject_metadata(img_path, meta["h1"] or meta["title"], meta["desc"])
                    total_kb_saved += (old_size - new_size)
                    optimized_imgs += 1

        new_html = upgrade_html(slug, html, meta)
        if new_html != html:
            f.write_text(new_html, encoding="utf-8")
            upgraded_html += 1

    print(f"Old blogs upgraded:")
    print(f"  HTML upgrades: {upgraded_html}")
    print(f"  Images optimized: {optimized_imgs} (saved {total_kb_saved} KB)")
    print(f"  New blogs skipped (already done): {skipped_new}")
    print(f"  Total blog files: {len(blog_files)}")


if __name__ == "__main__":
    main()
