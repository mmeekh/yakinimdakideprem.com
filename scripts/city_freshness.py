#!/usr/bin/env python3
"""
city_freshness.py — Continuous worker.

Her 60 saniyede bir API'dan son depremleri çeker, 3.5+ büyüklükteki
depremin geçtiği şehir sayfasının statik HTML'ini günceller:

  • SSR-FRESHNESS bloğunu LiveBlogPosting schema + visible timestamp
    + "Az önce {büyüklük} deprem" passage ile doldurur (AI crawler'lar
    JS execute etmediği için bu kritik).
  • <title> ve <meta description>'ı freshness sinyali için günceller.
  • sitemap.xml'de o şehir URL'sinin lastmod'unu bumplar.
  • IndexNow API'sine ping atar (Bing/Yandex anlık).

Kullanım:
  INDEXNOW_KEY=xxx python3 scripts/city_freshness.py            # daemon
  python3 scripts/city_freshness.py --once                      # tek tur
  python3 scripts/city_freshness.py --simulate-quake istanbul   # test
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import requests

# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
ALIASES_FILE = ROOT / "scripts" / "city_aliases.json"
SITEMAP = PUBLIC / "sitemap.xml"

API_URL = os.getenv(
    "FRESHNESS_API_URL",
    "http://yakinimdakideprem-api:8000/api/earthquakes",
)
POLL_SECONDS = int(os.getenv("FRESHNESS_POLL_SECONDS", "60"))
MIN_MAGNITUDE = float(os.getenv("FRESHNESS_MIN_MAGNITUDE", "3.5"))
HOURS_BACK = int(os.getenv("FRESHNESS_HOURS_BACK", "6"))
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY", "")
INDEXNOW_HOST = "yakinimdakideprem.com"
TZ_TR = timezone(timedelta(hours=3))

SSR_START = "<!-- SSR-FRESHNESS-START -->"
SSR_END = "<!-- SSR-FRESHNESS-END -->"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("freshness")


# ----------------------------------------------------------------------
def normalize(text: str) -> str:
    """Lowercase + strip Turkish diacritics (Kandilli'nin ASCII'sine eşleşir)."""
    if not text:
        return ""
    text = text.lower()
    table = str.maketrans({"ı": "i", "ş": "s", "ç": "c",
                            "ö": "o", "ü": "u", "ğ": "g", "İ": "i"})
    text = text.translate(table)
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def load_cities() -> dict:
    return json.loads(ALIASES_FILE.read_text(encoding="utf-8"))


def find_city_slug(place: str, cities: dict) -> Optional[str]:
    """Match a Kandilli place string to a city slug via alias longest-match."""
    place_norm = normalize(place)
    best = None
    best_len = 0
    for slug, info in cities.items():
        for alias in info["aliases"]:
            alias_norm = normalize(alias)
            if alias_norm and alias_norm in place_norm and len(alias_norm) > best_len:
                best = slug
                best_len = len(alias_norm)
    return best


def fetch_recent_quakes() -> list:
    params = {"hours_back": HOURS_BACK, "min_magnitude": MIN_MAGNITUDE, "limit": 50}
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("data", []) or []
    except Exception as e:
        log.error(f"API fetch failed: {e}")
        return []


def parse_quake_time(raw: str) -> datetime:
    """Kandilli '2026.05.05 14:32:00' → tz-aware datetime."""
    if not raw:
        return datetime.now(TZ_TR)
    raw = raw.replace(".", "-").strip()
    try:
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=TZ_TR)
        return dt
    except ValueError:
        return datetime.now(TZ_TR)


def humanize_minutes_ago(dt: datetime) -> str:
    delta = datetime.now(TZ_TR) - dt
    minutes = int(delta.total_seconds() // 60)
    if minutes < 1:
        return "Az önce"
    if minutes < 60:
        return f"{minutes} dakika önce"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} saat önce"
    return f"{hours // 24} gün önce"


# ----------------------------------------------------------------------
def build_ssr_block(slug: str, city_name: str, quake: dict) -> str:
    mag = float(quake.get("magnitude", 0) or 0)
    place = quake.get("location") or quake.get("place") or "Bilinmeyen"
    # Derinlik fallback: boş/None değer "km" göstermesin
    depth_raw = quake.get("depth", "")
    if depth_raw in (None, "", 0, "0"):
        depth_display = "Bilinmiyor"
        depth_text = ""   # passage'da göstermez
    else:
        try:
            depth_display = f"{float(depth_raw):.1f} km"
            depth_text = f" Derinlik: {depth_display}."
        except (TypeError, ValueError):
            depth_display = str(depth_raw)
            depth_text = f" Derinlik: {depth_display}."

    qtime = parse_quake_time(quake.get("time", ""))
    iso = qtime.isoformat()
    iso_now = datetime.now(TZ_TR).isoformat()
    pretty = qtime.strftime("%d %B %Y, %H:%M") + " TSİ"
    ago = humanize_minutes_ago(qtime)

    canonical = f"https://yakinimdakideprem.com/deprem-{slug}.html"
    # liveBlogUpdate item için kalıcı anchor URL
    update_anchor = f"{canonical}#update-{qtime.strftime('%Y%m%dT%H%M%S')}"

    schema = {
        "@context": "https://schema.org",
        "@type": "LiveBlogPosting",
        "@id": f"{canonical}#liveblog",
        "headline": f"{city_name} Deprem Takibi — Canlı",
        "datePublished": iso,
        "dateModified": iso_now,
        "coverageStartTime": iso,
        "url": canonical,
        "image": f"https://yakinimdakideprem.com/images/cities/{slug}-og.webp",
        "about": {"@type": "Place", "name": city_name, "addressCountry": "TR"},
        "author": {
            "@type": "Person",
            "name": "Emin Kılıç",
            "url": "https://yakinimdakideprem.com/ben-kimim.html",
            "@id": "https://yakinimdakideprem.com/ben-kimim.html#person",
        },
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "@id": "https://yakinimdakideprem.com/#organization",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png",
                "width": 512,
                "height": 512,
            },
        },
        "liveBlogUpdate": [{
            "@type": "BlogPosting",
            "@id": update_anchor,
            "url": update_anchor,
            "headline": f"{city_name} {mag:.1f} büyüklüğünde deprem",
            "datePublished": iso,
            "articleBody": (
                f"{ago}, {place} bölgesinde {mag:.1f} büyüklüğünde deprem "
                f"kaydedildi.{depth_text}".strip()
            ),
        }],
    }

    return (
        f"{SSR_START}\n"
        '            <div class="ssr-freshness" itemscope '
        'itemtype="https://schema.org/Event" aria-live="polite">\n'
        f'                <p class="ssr-freshness__alert">'
        f'🔴 <strong>{ago}:</strong> '
        f'<span itemprop="name">{city_name} {mag:.1f} büyüklüğünde deprem</span> — '
        f'<span itemprop="location">{place}</span>'
        f'{f" • Derinlik: {depth_display}" if depth_text else ""}.'
        f'</p>\n'
        f'                <time class="ssr-freshness__time" '
        f'itemprop="startDate" datetime="{iso}">'
        f'Deprem zamanı: {pretty}</time>\n'
        '            </div>\n'
        '            <script type="application/ld+json">\n'
        f'            {json.dumps(schema, ensure_ascii=False, indent=2)}\n'
        '            </script>\n'
        f"            {SSR_END}"
    )


def build_quake_table_rows(quakes_for_city: list) -> str:
    """Şehir tbody'sine yerleştirilecek son 5 deprem HTML satırı."""
    if not quakes_for_city:
        return '<tr><td colspan="4">Bu şehir için kayıtlı son deprem bulunamadı.</td></tr>'

    rows = []
    for q in quakes_for_city[:5]:
        mag = float(q.get("magnitude", 0) or 0)
        place = q.get("location") or q.get("place") or "Bilinmiyor"
        depth = q.get("depth", "?")
        try:
            depth_str = f"{float(depth):.1f} km"
        except (TypeError, ValueError):
            depth_str = "—"
        qtime = parse_quake_time(q.get("time", ""))
        time_str = qtime.strftime("%d.%m.%Y %H:%M")
        rows.append(
            f'<tr><td>{time_str}</td>'
            f'<td><strong>M{mag:.1f}</strong></td>'
            f'<td>{depth_str}</td>'
            f'<td>{place}</td></tr>'
        )
    return "\n                                ".join(rows)


def update_city_page(slug: str, city_name: str, quake: dict,
                       quakes_for_city: list = None) -> bool:
    page = PUBLIC / f"deprem-{slug}.html"
    if not page.exists():
        return False

    html = page.read_text(encoding="utf-8")
    if SSR_START not in html:
        log.warning(f"{slug}: SSR placeholder yok, atlanıyor")
        return False

    # Replace the SSR block
    new_block = build_ssr_block(slug, city_name, quake)
    new_html = re.sub(
        re.escape(SSR_START) + r".*?" + re.escape(SSR_END),
        new_block,
        html,
        count=1,
        flags=re.DOTALL,
    )

    # SSR quake table: AI crawler'lar için tbody içine son 5 deprem inject et.
    # JS yine renderCityQuakes ile dinamik update yapar; bu sadece initial render.
    if quakes_for_city:
        rows_html = build_quake_table_rows(quakes_for_city)
        new_html = re.sub(
            r'(<tbody id="' + re.escape(slug) + r'-quakes">)\s*'
            r'(?:<tr><td colspan="4">[^<]+</td></tr>|.*?)\s*(</tbody>)',
            rf'\1\n                                {rows_html}\n                            \2',
            new_html,
            count=1,
            flags=re.DOTALL,
        )

    # Title freshness: SADECE M4.0+ depremlerde dinamik title. Aksi halde
    # standart CTR-optimize başlık. Bu, küçük (M1-2) depremlerin SERP'te
    # sayfa başlığını kötüleştirmesini önler.
    mag = float(quake.get("magnitude", 0) or 0)
    if mag >= 4.0:
        new_title = (
            f"🔴 {city_name}'da Az Önce {mag:.1f} Deprem | Anlık Deprem Takibi"
        )
    else:
        # Standart CTR-optimize başlık
        new_title = (
            f"Anlık Deprem {city_name} 🔴 Canlı Harita ve Son Depremler"
        )
    new_html = re.sub(
        r"<title>[^<]+</title>",
        f"<title>{new_title}</title>",
        new_html,
        count=1,
    )

    if new_html == html:
        return False

    # Atomic write
    tmp = page.with_suffix(".html.tmp")
    tmp.write_text(new_html, encoding="utf-8")
    tmp.replace(page)
    return True


def update_sitemap(slug: str) -> bool:
    if not SITEMAP.exists():
        return False
    text = SITEMAP.read_text(encoding="utf-8")
    today = datetime.now(TZ_TR).strftime("%Y-%m-%d")
    pattern = re.compile(
        r"(<loc>https://yakinimdakideprem\.com/deprem-"
        + re.escape(slug) + r"\.html</loc>\s*<lastmod>)[^<]+(</lastmod>)"
    )
    new_text, n = pattern.subn(rf"\g<1>{today}\g<2>", text)
    if n > 0 and new_text != text:
        SITEMAP.write_text(new_text, encoding="utf-8")
        return True
    return False


def ping_indexnow(slug: str):
    if not INDEXNOW_KEY:
        return
    url = f"https://yakinimdakideprem.com/deprem-{slug}.html"
    payload = {
        "host": INDEXNOW_HOST,
        "key": INDEXNOW_KEY,
        "urlList": [url, "https://yakinimdakideprem.com/"],
    }
    try:
        r = requests.post("https://api.indexnow.org/indexnow",
                          json=payload, timeout=8)
        log.info(f"IndexNow ping {slug}: HTTP {r.status_code}")
    except Exception as e:
        log.warning(f"IndexNow failed: {e}")


# ----------------------------------------------------------------------
def update_homepage(quakes: list, cities: dict) -> bool:
    """Anasayfaya son 5 önemli depremin statik listesini enjekte et.
    AI crawler'lar JS execute etmediği için bu kritik freshness sinyali."""
    page = PUBLIC / "index.html"
    if not page.exists() or not quakes:
        return False
    html = page.read_text(encoding="utf-8")
    if SSR_START not in html:
        return False

    # Top 5 by time
    items = []
    now_iso = datetime.now(TZ_TR).isoformat()
    for q in quakes[:5]:
        place = q.get("location") or q.get("place") or "Bilinmiyor"
        mag = float(q.get("magnitude", 0) or 0)
        depth = q.get("depth", "?")
        qtime = parse_quake_time(q.get("time", ""))
        ago = humanize_minutes_ago(qtime)
        slug = find_city_slug(place, cities)
        href = f"/deprem-{slug}.html" if slug else "#"
        items.append((mag, place, depth, qtime, ago, href))

    if not items:
        return False

    latest = items[0]
    list_html = "\n".join([
        f'                <li class="hp-fresh__item">'
        f'<a href="{href}"><strong>{place}</strong></a> '
        f'— <span class="hp-fresh__mag">M{mag:.1f}</span> '
        f'<time datetime="{qt.isoformat()}">{ago}</time> '
        f'<span class="hp-fresh__depth">• {depth} km</span></li>'
        for mag, place, depth, qt, ago, href in items
    ])

    schema = {
        "@context": "https://schema.org",
        "@type": "LiveBlogPosting",
        "headline": "Türkiye Anlık Deprem Takibi — Canlı",
        "datePublished": latest[3].isoformat(),
        "dateModified": now_iso,
        "coverageStartTime": latest[3].isoformat(),
        "about": {"@type": "Place", "name": "Türkiye"},
        "author": {"@type": "Organization", "name": "Yakınımdaki Deprem"},
        "publisher": {
            "@type": "Organization",
            "name": "Yakınımdaki Deprem",
            "logo": {
                "@type": "ImageObject",
                "url": "https://yakinimdakideprem.com/icons/android-chrome-512x512.png",
            },
        },
        "liveBlogUpdate": [{
            "@type": "BlogPosting",
            "headline": f"{place} M{mag:.1f}",
            "datePublished": qt.isoformat(),
            "articleBody": f"{ago}, {place} bölgesinde {mag:.1f} büyüklüğünde "
                           f"deprem kaydedildi. Derinlik: {depth} km.",
        } for mag, place, depth, qt, ago, _ in items],
    }

    block = (
        f"{SSR_START}\n"
        '    <section class="ssr-homepage-freshness" aria-live="polite">\n'
        '        <div class="container">\n'
        '            <h2 class="hp-fresh__title">'
        '🔴 Türkiye\'de Son 5 Önemli Deprem</h2>\n'
        '            <ul class="hp-fresh__list">\n'
        f"{list_html}\n"
        '            </ul>\n'
        f'            <p class="hp-fresh__updated">Son güncelleme: '
        f'<time datetime="{now_iso}">'
        f'{datetime.now(TZ_TR).strftime("%d.%m.%Y %H:%M")} TSİ</time></p>\n'
        '        </div>\n'
        '    </section>\n'
        '    <script type="application/ld+json">\n'
        f'    {json.dumps(schema, ensure_ascii=False)}\n'
        '    </script>\n'
        f"    {SSR_END}"
    )

    new_html = re.sub(
        re.escape(SSR_START) + r".*?" + re.escape(SSR_END),
        block,
        html,
        count=1,
        flags=re.DOTALL,
    )
    if new_html == html:
        return False

    tmp = page.with_suffix(".html.tmp")
    tmp.write_text(new_html, encoding="utf-8")
    tmp.replace(page)
    return True


# Deduplication state — process'in hayatı boyunca aynı (slug, quake_id) tekrar
# yazılmasın (gereksiz disk I/O + IndexNow rate limit'ten kaçın).
_LAST_WRITTEN: dict[str, str] = {}   # slug → last quake_id
_LAST_HOMEPAGE: tuple = None         # (top_quake_id, ...) tuple of latest 5 ids


def run_once(cities: dict) -> int:
    """One pass: process the most recent quake per city + update homepage.
    Deduplication: aynı deprem ID'si tekrar yazılmaz."""
    global _LAST_HOMEPAGE
    quakes = fetch_recent_quakes()
    if not quakes:
        return 0

    quakes.sort(key=lambda q: q.get("time", ""), reverse=True)

    # ----- Anasayfa: top 5'in ID-set'i değiştiyse güncelle -----
    homepage_pool = [q for q in quakes
                     if float(q.get("magnitude", 0) or 0) >= MIN_MAGNITUDE]
    top5_ids = tuple(q.get("id") for q in homepage_pool[:5])
    if top5_ids and top5_ids != _LAST_HOMEPAGE:
        if update_homepage(homepage_pool, cities):
            log.info(f"✓ Anasayfa güncellendi (son {len(top5_ids)} deprem)")
            ping_indexnow_url("https://yakinimdakideprem.com/")
            _LAST_HOMEPAGE = top5_ids

    # ----- Şehir sayfaları: her şehir için en yeni deprem (M3.5+) -----
    # quakes_by_city: slug → en yeni 5 deprem (SSR quake table için)
    quakes_by_city: dict[str, list] = {}
    for q in quakes:
        place = q.get("location") or q.get("place") or ""
        slug = find_city_slug(place, cities)
        if slug:
            quakes_by_city.setdefault(slug, []).append(q)

    seen = set()
    updated = 0

    for q in quakes:
        try:
            mag = float(q.get("magnitude", 0) or 0)
        except (TypeError, ValueError):
            continue
        if mag < MIN_MAGNITUDE:
            continue

        place = q.get("location") or q.get("place") or ""
        slug = find_city_slug(place, cities)
        if not slug or slug in seen:
            continue
        seen.add(slug)

        qid = q.get("id") or place
        if _LAST_WRITTEN.get(slug) == qid:
            continue   # zaten bu deprem yazılı, atla

        city_name = cities[slug]["name"]
        city_quakes = quakes_by_city.get(slug, [])
        if update_city_page(slug, city_name, q, quakes_for_city=city_quakes):
            update_sitemap(slug)
            ping_indexnow(slug)
            _LAST_WRITTEN[slug] = qid
            log.info(
                f"✓ {slug:15s} M{mag:>3.1f} {place[:50]}"
            )
            updated += 1
    return updated


def ping_indexnow_url(url: str):
    if not INDEXNOW_KEY:
        return
    try:
        requests.post(
            "https://api.indexnow.org/indexnow",
            json={"host": INDEXNOW_HOST, "key": INDEXNOW_KEY, "urlList": [url]},
            timeout=8,
        )
    except Exception:
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--once", action="store_true", help="Tek tur, daemon değil")
    p.add_argument("--simulate-quake", metavar="SLUG",
                   help="Belirtilen şehir için sahte deprem inject et (test)")
    args = p.parse_args()

    cities = load_cities()
    log.info(f"Loaded {len(cities)} cities. API={API_URL} threshold=M{MIN_MAGNITUDE}")

    if args.simulate_quake:
        slug = args.simulate_quake
        if slug not in cities:
            log.error(f"Unknown slug: {slug}")
            sys.exit(1)
        fake = {
            "magnitude": 4.2,
            "place": f"TEST-{cities[slug]['name'].upper()}",
            "location": f"TEST-{cities[slug]['name'].upper()}",
            "time": datetime.now(TZ_TR).strftime("%Y-%m-%d %H:%M:%S"),
            "depth": "8.5",
            "id": "test-quake",
        }
        # SSR quake table testi için fake liste de geçir
        fake_list = [fake] * 3
        update_city_page(slug, cities[slug]["name"], fake,
                          quakes_for_city=fake_list)
        update_sitemap(slug)
        log.info(f"Simulated quake injected into deprem-{slug}.html")
        return

    if args.once:
        run_once(cities)
        return

    log.info(f"Daemon başladı, her {POLL_SECONDS}s API check.")
    while True:
        try:
            run_once(cities)
        except Exception as e:
            log.exception(f"Loop error: {e}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
