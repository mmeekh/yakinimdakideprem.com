#!/usr/bin/env python3
"""
A-Z audit fix'lerini tüm blog + şehir sayfalarına uygula:
1. YMYL inline disclaimer (hayat kurtaran içerikli sayfalara)
2. <img alt> attribute fetchpriority="high" hero görselleri için
"""
import re
from pathlib import Path

PUBLIC = Path("/root/projects/yakinimdakideprem.com/public")

# YMYL disclaimer — sadece güvenlik/hayat-kurtaran konular için
YMYL_KEYWORDS = [
    "aninda", "cantasi", "icindeyseniz", "disaridaysaniz", "arac",
    "asansor", "yatakta", "balkon", "oncesi-hazirlik", "sonrasi",
    "ilk-24-saat", "psikolojik", "engelli", "yaslilar", "kadinlar",
    "evcil", "cocuklar", "okul", "apartman-yoneticisi",
]

DISCLAIMER_BLOCK = """
                <aside class="ymyl-disclaimer" role="note" aria-label="Önemli uyarı">
                    <p class="ymyl-disclaimer__title">⚠️ Önemli Uyarı</p>
                    <p>Bu içerik <strong>genel bilgilendirme ve hazırlık</strong> amaçlıdır; profesyonel acil durum, tıbbi veya hukuki tavsiye yerine geçmez. <strong>Acil durumda 112'yi arayın</strong> ya da <a href="https://deprem.afad.gov.tr" target="_blank" rel="noopener noreferrer">AFAD</a> yönergelerine uyun. Bina güçlendirme, tıbbi acil durum veya hukuki süreçler için <strong>ilgili uzmana danışın</strong>.</p>
                </aside>
"""

DISCLAIMER_MARKER = '<aside class="ymyl-disclaimer"'

def is_ymyl_blog(slug: str) -> bool:
    return any(kw in slug for kw in YMYL_KEYWORDS)


def inject_disclaimer(html: str) -> tuple[str, bool]:
    if DISCLAIMER_MARKER in html:
        return html, False
    # İlk <p class="lead">'ten sonra ya da <article> başında ekle
    new_html, n = re.subn(
        r'(<p class="lead">[^<]*</p>)',
        r'\1\n' + DISCLAIMER_BLOCK.rstrip(),
        html, count=1,
    )
    if n == 0:
        # Fallback: <article>'tan sonra
        new_html, n = re.subn(
            r'(<article[^>]*>)',
            r'\1\n' + DISCLAIMER_BLOCK.rstrip(),
            html, count=1,
        )
    return new_html, n > 0


def add_fetchpriority_to_hero(html: str) -> tuple[str, bool]:
    """Hero görseline fetchpriority='high' ekle (LCP optimizasyonu)."""
    if 'fetchpriority="high"' in html:
        return html, False
    # <picture> içindeki <img>'ye ekle
    new_html, n = re.subn(
        r'(<picture>\s*<img\s+src="[^"]+"\s+alt="[^"]+"\s+)(width)',
        r'\1fetchpriority="high" \2',
        html, count=1,
    )
    return new_html, n > 0


def main():
    blog_files = sorted(PUBLIC.glob("blog-*.html"))
    disclaimer_added = 0
    fetchpriority_added = 0
    total = 0

    for f in blog_files:
        slug = f.stem
        total += 1
        html = f.read_text(encoding="utf-8")
        new_html = html

        if is_ymyl_blog(slug):
            new_html, changed = inject_disclaimer(new_html)
            if changed:
                disclaimer_added += 1

        new_html, fp_changed = add_fetchpriority_to_hero(new_html)
        if fp_changed:
            fetchpriority_added += 1

        if new_html != html:
            f.write_text(new_html, encoding="utf-8")

    print(f"Total blog files: {total}")
    print(f"YMYL disclaimer added: {disclaimer_added}")
    print(f"fetchpriority='high' added: {fetchpriority_added}")


if __name__ == "__main__":
    main()
