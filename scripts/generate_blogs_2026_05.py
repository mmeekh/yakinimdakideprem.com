#!/usr/bin/env python3
"""
10 yeni blog için HTML generator (2026-05 batch).

Her blog config:
  slug, title, meta_description, keywords, category, image_alt,
  lead, body_h2_blocks (list of (h2, paragraphs)), faqs (list of (q, a)).

Çıktı: public/blog-{slug}.html (SEO-tam, schema.org BlogPosting+FAQPage+Breadcrumb)
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

TODAY = date.today().isoformat()
PUBLISH_DATE = "2026-05-05"


def html_escape(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))


def build_html(cfg: dict) -> str:
    slug = cfg["slug"]
    title = cfg["title"]
    desc = cfg["meta_description"]
    kws = cfg["keywords"]
    img = f"images/blog-{slug}.webp"
    canonical = f"https://yakinimdakideprem.com/blog-{slug}.html"

    # ----- BlogPosting schema -----
    schema_blog = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": desc,
        "image": {
            "@type": "ImageObject",
            "url": f"https://yakinimdakideprem.com/{img}",
            "width": 1536,
            "height": 1024,
            "caption": title,
            "creditText": "Yakınımdaki Deprem",
            "creator": {
                "@type": "Person",
                "name": "Emin Kılıç",
                "url": "https://yakinimdakideprem.com/ben-kimim.html",
            },
            "copyrightHolder": {"@type": "Organization", "name": "Yakınımdaki Deprem"},
        },
        "author": {
            "@type": "Person",
            "name": "Emin Kılıç",
            "url": "https://yakinimdakideprem.com/ben-kimim.html",
        },
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "url": "https://yakinimdakideprem.com",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png",
                "width": 512,
                "height": 512,
            },
        },
        "datePublished": PUBLISH_DATE,
        "dateModified": PUBLISH_DATE,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "keywords": ", ".join(kws),
        "inLanguage": "tr-TR",
    }

    schema_breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ana Sayfa",
             "item": "https://yakinimdakideprem.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog",
             "item": "https://yakinimdakideprem.com/blog.html"},
            {"@type": "ListItem", "position": 3, "name": title},
        ],
    }

    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in cfg["faqs"]
        ],
    }

    # ----- Body H2 blocks -----
    body_html = ""
    for h2, paragraphs in cfg["body_h2_blocks"]:
        body_html += f'\n                <h2>{h2}</h2>\n'
        for p in paragraphs:
            body_html += f'                <p>{p}</p>\n'

    # ----- FAQ visible block -----
    faq_html = ""
    for q, a in cfg["faqs"]:
        faq_html += f'\n                    <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>'

    related_html = "\n".join([
        f'                    <li><a href="{href}">{label}</a></li>'
        for href, label in cfg.get("related", [
            ("/blog-deprem-oncesi-hazirlik.html", "Deprem Öncesi Hazırlık"),
            ("/blog-deprem-cantasi.html", "Deprem Çantası Listesi 2026"),
            ("/blog.html", "Tüm Deprem Rehberleri"),
        ])
    ])

    return dedent(f"""\
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#ffffff">
    <title>{html_escape(title)}</title>
    <meta name="description" content="{html_escape(desc)}">
    <meta name="keywords" content="{html_escape(', '.join(kws))}">
    <meta name="author" content="Emin Kılıç">
    <link rel="canonical" href="{canonical}" />
    <meta property="og:locale" content="tr_TR">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{html_escape(title)}">
    <meta property="og:description" content="{html_escape(desc)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="Yakınımdaki Deprem">
    <meta property="og:image" content="https://yakinimdakideprem.com/{img}">
    <meta property="og:image:alt" content="{html_escape(cfg['image_alt'])}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html_escape(title)}">
    <meta name="twitter:description" content="{html_escape(desc)}">
    <meta name="twitter:image" content="https://yakinimdakideprem.com/{img}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <link rel="stylesheet" href="css/style.min.css?v=202605051900">
    <link rel="stylesheet" href="css/header.min.css?v=202605051900">
    <link rel="stylesheet" href="css/blog-detail.css?v=2026011231">
    <link rel="stylesheet" href="css/city-search.css?v=202604202200">
    <link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32x32.png">
    <link rel="manifest" href="site.webmanifest">
    <script type="application/ld+json">
{json.dumps(schema_blog, ensure_ascii=False, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(schema_breadcrumb, ensure_ascii=False, indent=2)}
    </script>
    <script type="application/ld+json">
{json.dumps(schema_faq, ensure_ascii=False, indent=2)}
    </script>
</head>
<body>
    <header id="hidden-header">
        <div class="container">
            <a href="/" class="logo"><img src="icons/logo.png" alt="Yakınımdaki Deprem" width="50" height="50"><span data-text="Yakınımdaki Deprem">Yakınımdaki Deprem</span></a>
            <div id="city-search" class="city-search" role="search">
                <div class="city-search__bar">
                    <i class="fas fa-search city-search__icon" aria-hidden="true"></i>
                    <label for="city-search-input" class="sr-only">Şehir ara</label>
                    <input type="text" id="city-search-input" placeholder="Şehir Ara 🏙️" autocomplete="off" aria-autocomplete="list" aria-controls="city-search-results">
                    <button type="button" id="city-search-clear" aria-label="Temizle" hidden><i class="fas fa-times" aria-hidden="true"></i></button>
                </div>
                <ul id="city-search-results" class="city-search__results" role="listbox" hidden></ul>
            </div>
            <nav>
                <a href="/">Ana Sayfa</a>
                <a href="/son-dakika-deprem.html" class="nav-highlight nav-alert">Son Dakika <span class="alarm-dot" aria-hidden="true"></span></a>
                <div class="nav-dropdown nav-dropdown-guides">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">Rehberler <i class="fas fa-chevron-down"></i></button>
                    <div class="dropdown-menu">
                        <a href="/deprem-aninda.html">Deprem Anında</a>
                        <a href="/ilk-yardim-cantasi.html">İlk Yardım Çantası</a>
                        <a href="/blog.html">Blog</a>
                    </div>
                </div>
                <div class="nav-dropdown">
                    <button class="dropdown-toggle" type="button" aria-haspopup="true" aria-expanded="false">Şehir Depremleri <i class="fas fa-chevron-down"></i></button>
                    <div class="dropdown-menu">
                        <a href="/deprem-sehirleri.html"><strong>📍 Tüm 81 İl</strong></a>
                        <a href="/deprem-istanbul.html">İstanbul</a>
                        <a href="/deprem-izmir.html">İzmir</a>
                        <a href="/deprem-ankara.html">Ankara</a>
                    </div>
                </div>
            </nav>
        </div>
    </header>
    <main class="blog-detail-container">
        <article>
            <div class="blog-hero" style="background-image: url('{img}');">
                <div class="overlay"></div>
                <div class="hero-content">
                    <h1>{html_escape(title)}</h1>
                    <div class="meta">
                        <span><i class="far fa-calendar" aria-hidden="true"></i> {PUBLISH_DATE}</span>
                        <span><i class="far fa-user" aria-hidden="true"></i> Emin Kılıç</span>
                    </div>
                </div>
            </div>
            <div class="content container">
                <p class="lead">{cfg["lead"]}</p>
{body_html}
                <h2>Sıkça Sorulan Sorular</h2>
                <div class="faq-list">{faq_html}
                </div>

                <h2>İlgili Rehberler</h2>
                <ul>
{related_html}
                </ul>
            </div>
        </article>
    </main>
    <footer>
        <div class="container">
            <p>&copy; 2026 Yakınımdaki Deprem. Tüm hakları saklıdır.</p>
        </div>
    </footer>
    <script src="js/header.min.js?v=202605051900" defer></script>
    <script src="js/city-keywords.js?v=202604202200" defer></script>
    <script src="js/city-search.js?v=202604202200" defer></script>
</body>
</html>
""")


def main(blogs: list[dict], force: bool = False, dry_run: bool = False):
    written: list[str] = []
    skipped: list[str] = []
    for cfg in blogs:
        out = PUBLIC / f"blog-{cfg['slug']}.html"
        if out.exists() and not force:
            print(f"  [atlandi] {out.name} (mevcut, --force ile uzerine yaz)")
            skipped.append(out.name)
            continue
        if dry_run:
            print(f"  [dry-run] would write {out}")
            written.append(out.name)
            continue
        out.write_text(build_html(cfg), encoding="utf-8")
        written.append(out.name)
    print(f"\n{'Would write' if dry_run else 'Wrote'} {len(written)} blog HTML files, skipped {len(skipped)}:")
    for w in written:
        prefix = "would-write" if dry_run else "wrote"
        print(f"  • [{prefix}] {w}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "config_file",
        nargs="?",
        default="scripts/blog_configs_2026_05.json",
        help="JSON config dosyasi (varsayilan: scripts/blog_configs_2026_05.json)",
    )
    parser.add_argument("--force", action="store_true", help="Mevcut dosyalari da yeniden yaz")
    parser.add_argument("--dry-run", action="store_true", help="Sadece listele, yazma")
    args = parser.parse_args()

    blogs = json.loads(Path(args.config_file).read_text(encoding="utf-8"))
    main(blogs, force=args.force, dry_run=args.dry_run)
