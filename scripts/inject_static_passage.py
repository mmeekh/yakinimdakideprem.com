#!/usr/bin/env python3
"""
Her şehir sayfasına AI Overviews / ChatGPT alıntı için optimize edilmiş
statik passage bloğu enjekte eder (140-160 kelime, soru-H2'lı, JS-free).

SEO ajan önerisi: Soru formatlı H2 + 2-3 cümlelik kendi-kendine yeterli passage,
AI crawler'ların alıntı seçimi için optimal. Statik HTML'de olması kritik —
JS-rendered içerik AI'lara görünmüyor.

Marker: <!-- SSR-PASSAGE-START --> ... <!-- SSR-PASSAGE-END -->
Idempotent: var olan blok atlanır (--force ile zorla yeniden yazılır).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ALIASES = ROOT / "scripts" / "city_aliases.json"

PSG_START = "<!-- SSR-PASSAGE-START -->"
PSG_END = "<!-- SSR-PASSAGE-END -->"


# Bölge → fay/risk özeti (passage'a serpilir)
REGION_RISK = {
    "Marmara": (
        "Kuzey Anadolu Fay Hattı'nın Marmara Denizi altından geçen kolu nedeniyle "
        "büyük deprem riski taşır. 1999 Gölcük ve Düzce depremleri bu hattın "
        "aktivitesinin somut göstergesidir."
    ),
    "Ege": (
        "Kuzey-güney yönlü normal fay sistemleri ve Ege Denizi'nin genişlemesi "
        "nedeniyle yüksek sismik aktivite gösterir. 2020 Samos-İzmir depremi bölgenin "
        "büyük yıkımlara açık olduğunu hatırlattı."
    ),
    "Akdeniz": (
        "Doğu Anadolu Fay Hattı'nın güney uzantıları ve Kıbrıs Yayı etkisi altındadır. "
        "6 Şubat 2023 Kahramanmaraş depremleri bölgenin tarihsel risklerini açıkça "
        "ortaya koydu."
    ),
    "İç Anadolu": (
        "Tuz Gölü Fay Zonu ve Kuzey Anadolu Fay Hattı'nın güney kolları arasında "
        "kalan, görece sakin fakat orta büyüklükte depremlere açık bir bölgedir."
    ),
    "Karadeniz": (
        "Kuzey Anadolu Fay Hattı'nın bölgeden geçen kolları nedeniyle orta-yüksek "
        "sismik risk taşır. 1942 Niksar-Erbaa ve 1943 Tosya-Ladik depremleri bu "
        "hattın bölgedeki yıkıcı etkisini göstermiştir."
    ),
    "Doğu Anadolu": (
        "Doğu Anadolu Fay Hattı (DAF) ile Kuzey Anadolu Fay Hattı'nın kesişim "
        "noktasında yer alır; 2023 Kahramanmaraş, 2011 Van depremleri bölgenin "
        "yüksek riskini doğrulamıştır."
    ),
    "Güneydoğu Anadolu": (
        "Doğu Anadolu Fay Hattı'nın güney kolları ile yerel fayların etkisi "
        "altındadır. 6 Şubat 2023 depremleri bölgenin sismik aktivitesinin yüksek "
        "olduğunu gösterdi."
    ),
}


def build_passage(slug: str, name: str, region: str) -> str:
    risk = REGION_RISK.get(region, "")
    canonical = f"https://yakinimdakideprem.com/deprem-{slug}.html"

    # 140-160 kelime hedefi
    text = (
        f"<section class=\"about-city-quakes\" id=\"about-{slug}-quakes\">\n"
        f"            <h2>{name} Depremleri Hakkında</h2>\n"
        f"            <p>Bu sayfa, AFAD (Afet ve Acil Durum Yönetimi Başkanlığı) ve "
        f"Kandilli Rasathanesi'nin (Boğaziçi Üniversitesi) yayımladığı resmi deprem "
        f"verilerini gerçek zamanlı olarak <strong>{name} ili ve çevresi</strong> "
        f"için filtreler. Veriler her 20 saniyede bir API üzerinden güncellenir; "
        f"büyüklük 1.0 ve üzeri tüm sarsıntılar otomatik listelenir. {risk} "
        f"Sayfada listelenen her depremin büyüklüğü, derinliği, merkez üssü ve oluş "
        f"zamanı gösterilir; harita üzerinde de işaretlenir.</p>\n"
        f"\n"
        f"            <h2>{name}'da Az Önce Deprem Mi Oldu?</h2>\n"
        f"            <p>Eğer sarsıntı hissettiyseniz, bu sayfanın yukarısındaki "
        f"\"Son Depremler\" listesine bakın. Liste her 20 saniyede bir yenilenir ve "
        f"<strong>{name}</strong> bölgesindeki en yeni kayıt en üstte görünür. "
        f"Verilerimiz Kandilli/AFAD'ın resmi API'lerinden alınır; gecikmesiz ve "
        f"birebirdir. Resmi açıklama için "
        f"<a href=\"https://deprem.afad.gov.tr\" target=\"_blank\" rel=\"noopener noreferrer\">AFAD</a> "
        f"sayfasını da kontrol edebilirsiniz. Yakınımızda meydana gelen depremlerde "
        f"<a href=\"/deprem-aninda.html\">Çök-Kapan-Tutun</a> kuralını uygulayın.</p>\n"
        f"        </section>"
    )

    return (
        f"{PSG_START}\n"
        f"        {text}\n"
        f"        {PSG_END}"
    )


def inject(slug: str, info: dict, force: bool) -> str:
    page = PUBLIC / f"deprem-{slug}.html"
    if not page.exists():
        return "missing"

    html = page.read_text(encoding="utf-8")
    has_existing = PSG_START in html

    if has_existing and not force:
        return "skipped"

    block = build_passage(slug, info["name"], info["region"])

    if has_existing:
        new_html = re.sub(
            re.escape(PSG_START) + r".*?" + re.escape(PSG_END),
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # Insert before </main> (or before footer if no main)
        if "</main>" in html:
            new_html = html.replace("</main>", f"{block}\n    </main>", 1)
        elif "<footer" in html:
            new_html = re.sub(r"(<footer)", block + r"\n    \1", html, count=1)
        else:
            return "no-anchor"

    if new_html == html:
        return "no-change"

    page.write_text(new_html, encoding="utf-8")
    return "injected"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true", help="Mevcut blokları yeniden yaz")
    p.add_argument("--slug")
    args = p.parse_args()

    cities = json.loads(ALIASES.read_text(encoding="utf-8"))
    targets = {args.slug: cities[args.slug]} if args.slug else cities

    counts = {"injected": 0, "skipped": 0, "missing": 0, "no-anchor": 0, "no-change": 0}
    for slug, info in targets.items():
        result = inject(slug, info, args.force)
        counts[result] = counts.get(result, 0) + 1

    print("Result:", counts)


if __name__ == "__main__":
    main()
